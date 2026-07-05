# Decisiones de Arquitectura — Backend AMLS

Este documento registra cómo el backend implementado se relaciona con
la Vista de Componentes y Vista de Despliegue de la propuesta original
(Diana Peralta, CINVESTAV), y qué decisiones se tomaron por restricciones
de tiempo/costo del prototipo de asignatura, para que puedan revisarse
conscientemente al continuar este proyecto en la tesis.

## Mapeo de componentes

| Componente en la propuesta | Implementación actual |
|---|---|
| API Gateway | `app/modules/gateway/` — agrega los routers de los demás módulos dentro del mismo proceso FastAPI |
| Content Manager | `app/modules/content/` |
| User Profile Manager | `app/modules/profile/` |
| ML Recommender Service | `app/modules/ml/` |
| Profile DB / History DB | Tablas en el mismo Postgres (actualmente alojado en Supabase, usado solo como Postgres estándar) |
| Content Repo (S3) | Pendiente — no implementado en esta fase del prototipo |

## Desviaciones conscientes respecto a la Vista de Despliegue original

1. **Un solo servicio, no 3 contenedores Docker independientes.**
   La propuesta especifica `Docker: Content Service`, `Docker: User Service`,
   `Docker: ML Service` como despliegues separados. En este prototipo,
   los tres viven como módulos dentro de un mismo proceso FastAPI
   ("monolito modular"), por restricciones de tiempo y para evitar
   costos/latencia de múltiples servicios gratuitos en frío.

   **Por qué esto no compromete la arquitectura a futuro:** cada módulo
   mantiene una interfaz de servicio propia y no accede directamente a
   las tablas de otro módulo. Separar un módulo a su propio contenedor
   más adelante implica envolver su interfaz existente en endpoints HTTP,
   no rediseñar su lógica interna.

2. **Postgres alojado en Supabase, usado únicamente como base de datos estándar.**
   No se usa el sistema de Auth, Storage ni API automática de Supabase.
   Esto mantiene la posibilidad de migrar a otro proveedor de Postgres
   (AWS RDS, un VPS propio, etc.) cambiando solo `DATABASE_URL`.

3. **Content Repo (S3) no implementado aún.**
   Pendiente de decidir su implementación cuando el proyecto lo requiera.

## Principios que se mantienen desde el día 1

- Toda configuración sensible/dependiente de entorno vive en variables
  de entorno (`.env` local, variables de entorno en despliegue), nunca
  hardcodeada.
- Todo cambio de esquema de base de datos se hace vía migraciones de
  Alembic, versionadas en el repositorio — no cambios manuales vía
  dashboard.
- Cada módulo (`content`, `profile`, `ml`, `gateway`) tiene una
  responsabilidad única que mapea 1:1 a un componente de la propuesta.
