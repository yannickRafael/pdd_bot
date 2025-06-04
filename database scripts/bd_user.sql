CREATE USER operador_funcoes WITH PASSWORD '123';

REVOKE ALL ON SCHEMA public FROM operador_funcoes;
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM operador_funcoes;
REVOKE ALL ON DATABASE pdd FROM operador_funcoes;

GRANT USAGE ON SCHEMA public TO operador_funcoes;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO operador_funcoes;
