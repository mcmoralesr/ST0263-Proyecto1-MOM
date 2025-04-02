#include "crow_all.h"
#include <sqlite3.h>
#include <iostream>

sqlite3* db;

void init_db() {
    int rc = sqlite3_open("mom1.db", &db);
    if (rc) {
        std::cerr << "Error al abrir la base de datos: " << sqlite3_errmsg(db) << std::endl;
        exit(1);
    }

    const char* create_topics = "CREATE TABLE IF NOT EXISTS topics (id INTEGER PRIMARY KEY, name TEXT UNIQUE);";
    const char* create_queues = "CREATE TABLE IF NOT EXISTS queues (id INTEGER PRIMARY KEY, name TEXT UNIQUE);";

    sqlite3_exec(db, create_topics, 0, 0, 0);
    sqlite3_exec(db, create_queues, 0, 0, 0);
}

int main() {
    init_db();

    crow::SimpleApp app;

    // Crear tópico
    CROW_ROUTE(app, "/topics").methods("POST"_method)([](const crow::request& req){
        auto body = crow::json::load(req.body);
        if (!body || !body.has("name")) {
            return crow::response(400, "Falta el nombre del tópico");
        }
        std::string name = body["name"].s();

        std::string sql = "INSERT INTO topics (name) VALUES (?);";
        sqlite3_stmt* stmt;
        if (sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, 0) != SQLITE_OK)
            return crow::response(500, "DB Error");
        sqlite3_bind_text(stmt, 1, name.c_str(), -1, SQLITE_STATIC);

        if (sqlite3_step(stmt) != SQLITE_DONE)
            return crow::response(400, "Tópico ya existe o error al insertar");

        sqlite3_finalize(stmt);
        return crow::response(200, "Tópico creado");
    });

    // Listar tópicos
    CROW_ROUTE(app, "/topics").methods("GET"_method)([](){
        std::string sql = "SELECT name FROM topics;";
        sqlite3_stmt* stmt;
        crow::json::wvalue result;
        int i = 0;

        if (sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, 0) == SQLITE_OK) {
            while (sqlite3_step(stmt) == SQLITE_ROW) {
                result[i++] = (const char*)sqlite3_column_text(stmt, 0);
            }
            sqlite3_finalize(stmt);
        }
        return crow::response(result);
    });

    // Crear cola
    CROW_ROUTE(app, "/queues").methods("POST"_method)([](const crow::request& req){
        auto body = crow::json::load(req.body);
        if (!body || !body.has("name")) {
            return crow::response(400, "Falta el nombre de la cola");
        }
        std::string name = body["name"].s();

        std::string sql = "INSERT INTO queues (name) VALUES (?);";
        sqlite3_stmt* stmt;
        if (sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, 0) != SQLITE_OK)
            return crow::response(500, "DB Error");
        sqlite3_bind_text(stmt, 1, name.c_str(), -1, SQLITE_STATIC);

        if (sqlite3_step(stmt) != SQLITE_DONE)
            return crow::response(400, "Cola ya existe o error al insertar");

        sqlite3_finalize(stmt);
        return crow::response(200, "Cola creada");
    });

    // Listar colas
    CROW_ROUTE(app, "/queues").methods("GET"_method)([](){
        std::string sql = "SELECT name FROM queues;";
        sqlite3_stmt* stmt;
        crow::json::wvalue result;
        int i = 0;

        if (sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, 0) == SQLITE_OK) {
            while (sqlite3_step(stmt) == SQLITE_ROW) {
                result[i++] = (const char*)sqlite3_column_text(stmt, 0);
            }
            sqlite3_finalize(stmt);
        }
        return crow::response(result);
    });

    app.port(18080).multithreaded().run();
    sqlite3_close(db);
}
