from unittest.mock import MagicMock, patch

from django.core.exceptions import ValidationError
from django.test import TestCase

from igrac.forms.groundwater_layer import CreateGroundwaterLayerForm


class CreateGroundwaterLayerFormNameValidationTest(TestCase):
    """Tests for the layer-name character validation in clean_name()."""

    def _clean_name(self, name):
        form = CreateGroundwaterLayerForm()
        form.cleaned_data = {'name': name}
        return form.clean_name()

    def test_rejects_comma(self):
        with self.assertRaises(ValidationError):
            self._clean_name('Well Data, Test')

    def test_rejects_colon(self):
        with self.assertRaises(ValidationError):
            self._clean_name('workspace:layer')

    def test_rejects_slash(self):
        with self.assertRaises(ValidationError):
            self._clean_name('layer/name')

    def test_rejects_quote(self):
        with self.assertRaises(ValidationError):
            self._clean_name("layer'name")

    def test_rejects_double_quote(self):
        with self.assertRaises(ValidationError):
            self._clean_name('layer"name')

    def test_rejects_ampersand(self):
        with self.assertRaises(ValidationError):
            self._clean_name('layer & name')

    def test_rejects_angle_brackets(self):
        with self.assertRaises(ValidationError):
            self._clean_name('<layer>')

    def test_rejects_leading_digit(self):
        with self.assertRaises(ValidationError):
            self._clean_name('1layer')

    def test_rejects_empty_name(self):
        with self.assertRaises(ValidationError):
            self._clean_name('')

    @patch('igrac.forms.groundwater_layer.gs_catalog')
    @patch('igrac.forms.groundwater_layer.SitePreference')
    def test_allows_letters_numbers_underscore_hyphen_space(
            self, mock_pref_model, mock_gs_catalog
    ):
        """A validly-formatted name must pass the character check and
        only fail later for an unrelated reason ("layer not found"),
        proving it was not rejected by the regex."""
        mock_pref = MagicMock()
        mock_pref.well_and_monitoring_data_layer.__str__.return_value = (
            'existing_layer'
        )
        mock_pref_model.objects.first.return_value = mock_pref
        mock_gs_catalog.get_layer.return_value = None

        with self.assertRaises(ValidationError) as ctx:
            self._clean_name('Valid_Layer-Name 123')
        self.assertIn('does not found', str(ctx.exception))