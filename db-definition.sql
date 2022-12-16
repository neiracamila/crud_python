 create database if not exists empleados;
 use empleados;
 
 create table empleados (
     id int not null auto_increment,
     nombre varchar(255), 
     correo varchar(255), 
     foto varchar (5000), 
     primary key (id)
     );


-- insert  into empleados (nombre, correo, foto) values
-- ('Mario', 'mario@email.com', 'fotodemario.jpg');
     
-- select * from empleados;
