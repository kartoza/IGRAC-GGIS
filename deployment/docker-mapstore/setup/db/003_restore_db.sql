/* SQL to insert user, groups, and profile */

INSERT INTO geostore.gs_usergroup (id,groupname,description,enabled) VALUES 
(1,'admin','admin','Y')
,(2,'user','user','Y')
;

INSERT INTO geostore.gs_user (id,"name",user_password,user_role,group_id,enabled) VALUES 
(1,'admin','admin','admin',1,'Y')
,(2,'user','user','user',2,'Y')
;

INSERT INTO geostore.gs_user_attribute (id,"name",string,user_id) VALUES 
(1,'admin','admin',1)
,(2,'user','user',2)
;

INSERT INTO geostore.gs_usergroup_members (user_id,group_id) VALUES 
(1,1)
,(2,2)
;
