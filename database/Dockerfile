FROM mcr.microsoft.com/mssql/server

ENV ACCEPT_EULA=Y
ENV SA_PASSWORD=YourStrong!Passw0rd
ENV MSSQL_PID=Developer

COPY init.sql /init.sql

CMD /opt/mssql/bin/sqlservr & sleep 30; /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P YourStrong!Passw0rd -d master -i /init.sql
