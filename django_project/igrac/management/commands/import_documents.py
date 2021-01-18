# coding=utf-8
import os
import requests
import tempfile
from django.core import files
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from geonode.documents.models import Document

User = get_user_model()


class Command(BaseCommand):
    """ Import document from a url list on the file.
    """
    help = 'Import document from a url list on the file.'

    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            type=str,
            help='Filename to be imported, it is in the fixtures.'
        )
        parser.add_argument(
            'owner',
            type=str,
            help='Indicates the username of owner of the document to be imported'
        )

    def handle(self, *args, **options):
        """Implementation for command.
        :param args:  Not used
        :param options: Not used
        """
        owner = options['owner']
        filename = options['filename']

        try:
            owner = User.objects.get(
                username=owner
            )
        except User.DoesNotExist:
            print('User does not found')
            return

        try:
            self.import_document(filename, owner)
        except FileNotFoundError:
            print('File does not found')
            return

    def import_document(self, filename, owner):
        """ Import document on the url list on the file
        filename should be always in the fixtures

        :param filename: name of file that will be imported
        :type filename: str

        :param owner: user as the owner
        :type owner: User
        """
        print('--------------------------------------------------------------')
        print('Importing {}.'.format(filename))
        print('--------------------------------------------------------------')

        django_root = os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            ))
        _file = os.path.join(
            django_root, 'fixtures', filename)
        f = open(_file, 'r')

        lines = f.readlines()
        for line in lines:
            line = line.replace('\n', '')
            print('-----------------------')
            print('check file : {}'.format(line))
            downloaded_filename = os.path.basename(line)
            downloaded_filename, ext = os.path.splitext(
                downloaded_filename)
            downloaded_filename = downloaded_filename + ext.split('_')[0]

            # skip request if document exist
            if Document.objects.filter(
                    title=downloaded_filename, owner=owner).count() == 0:

                # request the file
                temp_file = tempfile.NamedTemporaryFile()

                document = Document()
                document.owner = owner
                document.title = downloaded_filename
                document.doc_url = line

                # Read the streamed image in sections
                response = requests.get(line, stream=True)
                if response.status_code == requests.codes.ok:
                    for block in response.iter_content(1024 * 8):
                        if not block:
                            break
                        temp_file.write(block)

                    # safe it to document
                    document.doc_file.save(downloaded_filename, files.File(temp_file))
                else:
                    print('link is dead so just save the url')
                document.save()
            else:
                print('skip. found document with same name and owner')
