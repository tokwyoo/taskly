-- Crear la tabla "user"
CREATE TABLE "user" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar(50) NOT NULL,
  "email" varchar(255) UNIQUE NOT NULL,
  "email_verified" boolean NOT NULL DEFAULT false,
  "password" varchar(255) NOT NULL,
  "profile_picture" varchar(255),
  "bio" varchar(255),
  "verified" boolean NOT NULL DEFAULT false,
  "created_at" timestamp DEFAULT CURRENT_TIMESTAMP
);

-- Crear la tabla "token"
CREATE TYPE token_type AS ENUM ('verification', 'password_reset', 'email_change');

CREATE TABLE "token" (
  "id" SERIAL PRIMARY KEY,
  "user_id" int NOT NULL,
  "token" varchar(255) NOT NULL,
  "token_type" token_type NOT NULL,
  "created_at" timestamp DEFAULT CURRENT_TIMESTAMP,
  "expires_at" timestamp NOT NULL,
  "is_used" boolean NOT NULL DEFAULT false
);

-- Crear la tabla "session"
CREATE TABLE "session" (
  "id" SERIAL PRIMARY KEY,
  "user_id" int NOT NULL,
  "refresh_token" varchar(255),
  "device_info" varchar(255) NOT NULL,
  "ip_address" varchar(45) NOT NULL,
  "created_at" timestamp DEFAULT CURRENT_TIMESTAMP,
  "expires_at" timestamp,
  "last_accessed" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "is_revoked" boolean NOT NULL DEFAULT false
);

-- Crear la tabla "list"
CREATE TABLE "list" (
  "id" SERIAL PRIMARY KEY,
  "user_id" int NOT NULL,
  "title" varchar(255) NOT NULL,
  "created_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" boolean NOT NULL DEFAULT false,
  "deleted_at" timestamp
);

-- Crear la tabla "task"
CREATE TABLE "task" (
  "id" SERIAL PRIMARY KEY,
  "list_id" int NOT NULL,
  "title" varchar(255) NOT NULL,
  "created_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "due_date" timestamp,
  "frequency" jsonb,
  "notes" text,
  "is_completed" boolean NOT NULL DEFAULT false,
  "completed_at" timestamp,
  "is_deleted" boolean NOT NULL DEFAULT false,
  "deleted_at" timestamp
);

-- Crear la tabla "notification"
CREATE TYPE notification_type AS ENUM ('task_due', 'custom');

CREATE TABLE "notification" (
  "id" SERIAL PRIMARY KEY,
  "user_id" int NOT NULL,
  "type" notification_type NOT NULL,
  "title" varchar(255) NOT NULL,
  "created_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "message" text NOT NULL,
  "is_read" boolean NOT NULL DEFAULT false,
  "task_id" int
);

-- Agregar las claves foráneas
ALTER TABLE "token" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("id");

ALTER TABLE "session" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("id");

ALTER TABLE "list" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("id");

ALTER TABLE "task" ADD FOREIGN KEY ("list_id") REFERENCES "list" ("id");

ALTER TABLE "notification" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("id");

ALTER TABLE "notification" ADD FOREIGN KEY ("task_id") REFERENCES "task" ("id");
