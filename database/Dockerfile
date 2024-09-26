FROM mcr.microsoft.com/mssql/server

ENV ACCEPT_EULA=Y
ENV SA_PASSWORD=YourStrong!Passw0rd
ENV MSSQL_PID=Developer

COPY init.sql /init.sql

CMD /opt/mssql/bin/sqlservr & \
    sleep 30; \
    while ! /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P YourStrong!Passw0rd -d master -Q "SELECT 1"; do \
        echo "Waiting for SQL Server to start..."; \
        sleep 5; \
    done; \
    /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P YourStrong!Passw0rd -d master -i /init.sql
