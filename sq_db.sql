CREATE TABLE Clients (
    u_login varchar(255) PRIMARY KEY NOT NULL,
    u_password varchar(255)
);


INSERT INTO Clients (u_login, u_password) VALUES ('alex.e', '123');
INSERT INTO Clients (u_login, u_password) VALUES ('bot.admin', '123');
INSERT INTO Clients (u_login, u_password) VALUES ('ivan.p', '123');