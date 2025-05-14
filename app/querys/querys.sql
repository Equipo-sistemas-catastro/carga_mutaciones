--------------------------------------------------------
--CREA TABLA DE CARGA PLANO
--------------------------------------------------------
DROP TABLE IF EXISTS planos_turnos_mutaciones;
CREATE TABLE planos_turnos_mutaciones (
    id_tabla SERIAL PRIMARY KEY,
    id_radicacion TEXT,
	id_zre TEXT,
	id_1 TEXT,
	id_2 TEXT,
	id_matricula INT,
	cod_catastral TEXT,
	cod_naturaleza_juridica TEXT,
	naturaleza_juridica TEXT,
	mes INT,
	anio INT,
	fecha_calculada date,
	fecha_procesado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_mes ON planos_turnos_mutaciones(mes);
CREATE INDEX idx_anio ON planos_turnos_mutaciones(anio);
CREATE INDEX idx_anio_mes ON planos_turnos_mutaciones(anio, mes);
CREATE INDEX idx_cod_naturaleza_juridica ON planos_turnos_mutaciones(cod_naturaleza_juridica);
CREATE INDEX idx_fecha_calculada ON planos_turnos_mutaciones(fecha_calculada);
CREATE INDEX idx_matricula_plano ON planos_turnos_mutaciones(id_matricula);


--------------------------------------------------------
--CREA TABLA LOG DE CARGA
--------------------------------------------------------
DROP TABLE IF EXISTS log_cargaplano_mutaciones;
CREATE TABLE log_cargaplano_mutaciones (
    id_log SERIAL PRIMARY KEY,
    nombre_archivo TEXT NOT NULL,
    ruta_archivo TEXT,
    registros_leidos TEXT,  --INTEGER DEFAULT 0,
	estado INT,
    mensaje_error TEXT,
    fecha_registro_log TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_log_nombre_archivo ON log_cargaplano_mutaciones(nombre_archivo);
CREATE INDEX idx_log_fecha_registro_log ON log_cargaplano_mutaciones(fecha_registro_log);
CREATE INDEX idx_log_estado ON log_cargaplano_mutaciones(estado);

--------------------------------------------------------

--------------------------------------------------------
--CREA TABLA DE USUARIOS
--------------------------------------------------------
DROP TABLE IF EXISTS tbl_usuarios;
CREATE TABLE tbl_usuarios (
    id_log SERIAL,
    id_usuario INT PRIMARY KEY,
    nombre_usuario TEXT NOT NULL,
    correo_usuario TEXT NOT NULL,
    perfil_usuario TEXT,
    fecha_auditoria TIMESTAMP DEFAULT NOW()
);


---------------------------------------------------
--CREA TABLA MAESTRA NATURALEZA JURIDICA
---------------------------------------------------
DROP TABLE IF EXISTS naturaleza_juridica;
CREATE TABLE public.naturaleza_juridica
(
    id_tabla serial NOT NULL,
	id_naturaleza text,
    nm_naturaleza text,
    PRIMARY KEY (id_tabla)
);
CREATE INDEX idx_id_naturaleza ON naturaleza_juridica(id_naturaleza);

---------------------------------------------------
--INSERTA LAS DATOS DE NATURALEZA JURIDICA QUE SE NECESITAN ANALIZAR 
---------------------------------------------------
INSERT INTO public.naturaleza_juridica (id_naturaleza, nm_naturaleza)
SELECT DISTINCT ON (cod_naturaleza_juridica) cod_naturaleza_juridica, naturaleza_juridica
FROM public.planos_turnos_mutaciones
WHERE cod_naturaleza_juridica IN (
    '0107','0108','0109','0104','0110','0112','0113','0122',
    '0124','0125','0138','0139','0140','0141','0144','0146',
    '0163','0164','0168','0169','0172'
)
ORDER BY cod_naturaleza_juridica, naturaleza_juridica;

---------------------------------------------------

---------------------------------------------------
--CREA TABLA DE DISTRIBUCIONES DE MUTACIONES
---------------------------------------------------
DROP TABLE IF EXISTS public.tbl_distri_mutaciones;
CREATE TABLE IF NOT EXISTS public.tbl_distri_mutaciones
(
    cod_matricula integer NOT NULL,
    max_fecha_plano date,
    max_fecha_sap date,
    id_zre text COLLATE pg_catalog."default",
    cod_naturaleza_juridica text COLLATE pg_catalog."default",
    naturaleza_juridica character varying(100) COLLATE pg_catalog."default",
    anio integer,
    mes integer,
    id_usuario integer NOT NULL,
    fecha_distribucion date,
    CONSTRAINT fk_distri_usuarios FOREIGN KEY (id_usuario)
        REFERENCES public.tbl_usuarios (id_usuario) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

CREATE INDEX IF NOT EXISTS idx2_cod_matricula
    ON public.tbl_distri_mutaciones USING btree
    (cod_matricula ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx2_id_usuario

-- DROP INDEX IF EXISTS public.idx2_id_usuario;
CREATE INDEX IF NOT EXISTS idx2_id_usuario
    ON public.tbl_distri_mutaciones USING btree
    (id_usuario ASC NULLS LAST)
    TABLESPACE pg_default;



---------------------------------------------------
--CREA TABLA zcatt_compravtas
---------------------------------------------------
CREATE TABLE IF NOT EXISTS public.zcatt_compravtas
(
    "mandt." character varying(3) COLLATE pg_catalog."default",
    cd_propietario character varying(20) COLLATE pg_catalog."default",
    cd_comprador character varying(20) COLLATE pg_catalog."default",
    fc_mutacion date NOT NULL,
    hora_mutacion time without time zone NOT NULL,
    nm_matricula_pdi numeric(9,0),
    cd_relac_vendedo character varying(1) COLLATE pg_catalog."default",
    cd_relac_comprad character varying(1) COLLATE pg_catalog."default",
    porc_compra_vnta numeric(7,3),
    porc_actual numeric(7,3),
    cd_mutacion numeric(4,0),
    nm_escritura numeric(10,0),
    nm_doc_mutacion character varying(25) COLLATE pg_catalog."default",
    cd_tipo_document character varying(1) COLLATE pg_catalog."default",
    vl_compraventa numeric(17,2),
    usuario character varying(12) COLLATE pg_catalog."default",
    nm_consecutivo numeric(20,0)
)



---------------------------------------------------
--CREA UNA VISTA MATERIALIZADA PARA QUE SEA CONSULTADA
--POR LA API DE PYTHON consulta_mutaciones
---------------------------------------------------
--QUERY PARA HACER EL JOIN ENTRE LA TABLA DE POSTGRES 
--DE LOS PLANOS y SAP POR EL CÓDIGO DE MATRÍCULA 
-- TRAE LAS MATRICULAS DE LA TABLA DE LOS PLANOS
-- QUE TIENEN FECHA MAYOR A LA DE SAP zcatt_compravts
---------------------------------------------------
---------------------------------------------------
CREATE MATERIALIZED VIEW vw_compara_mutaciones AS
WITH ultimos_planos AS (
    SELECT DISTINCT ON (id_matricula)
        id_zre,
        id_matricula,
        cod_naturaleza_juridica,
        fecha_calculada,
        anio,
        mes
    FROM planos_turnos_mutaciones
    WHERE id_matricula IS NOT NULL
    ORDER BY id_matricula, fecha_calculada DESC
),
ultimas_compraventas AS (
    SELECT DISTINCT ON (nm_matricula_pdi)
        nm_matricula_pdi,
        fc_mutacion
    FROM zcatt_compravtas
    WHERE nm_matricula_pdi IS NOT NULL
    ORDER BY nm_matricula_pdi, fc_mutacion DESC
)
SELECT
    p.id_matricula AS cod_matricula,
    p.fecha_calculada AS max_fecha_plano,
    z.fc_mutacion AS max_fecha_SAP,
    p.id_zre,
    p.cod_naturaleza_juridica,
    nj.nm_naturaleza AS naturaleza_juridica,
    p.anio,
    p.mes
FROM ultimos_planos p
JOIN ultimas_compraventas z
    ON p.id_matricula = z.nm_matricula_pdi
INNER JOIN naturaleza_juridica nj
    ON p.cod_naturaleza_juridica = nj.id_naturaleza
WHERE p.fecha_calculada > z.fc_mutacion
ORDER BY p.id_matricula;


-- Índice por id_matricula
CREATE UNIQUE INDEX vw_compara_mutaciones_uidx
ON vw_compara_mutaciones (cod_matricula);



--SE NECESITA EJECUTAR CADA QUE SE CARGA UN ARCHIVO PLANO 
REFRESH MATERIALIZED VIEW CONCURRENTLY vw_compara_mutaciones



---------------------------------------------------
--CREA UN SP EN LA BD PARA DISTRIBUIR LAS MUTACIONES...
--A LOS USUARIOS SELECCIONADOS DESDE EL FRONTEND
---------------------------------------------------
CREATE OR REPLACE PROCEDURE sp_distribuir_mutaciones(p_id_usuarios INTEGER[])
LANGUAGE plpgsql
AS $$
DECLARE
    usuarios_validos INTEGER[];
    total_usuarios INT;
BEGIN
    -- Validar usuarios existentes
    SELECT ARRAY_AGG(id_usuario) INTO usuarios_validos
    FROM tbl_usuarios
    WHERE id_usuario = ANY(p_id_usuarios);

    IF usuarios_validos IS NULL OR array_length(usuarios_validos, 1) = 0 THEN
        RAISE EXCEPTION 'No se encontraron usuarios válidos en la tabla tbl_usuarios';
    END IF;

    total_usuarios := array_length(usuarios_validos, 1);

	-- Eliminar registros existentes para la fecha actual
    DELETE FROM tbl_distri_mutaciones
    WHERE fecha_distribucion = CURRENT_DATE;

    -- Insertar distribución en tbl_distri_mutaciones con fecha actual
    INSERT INTO tbl_distri_mutaciones (
        cod_matricula, max_fecha_plano, max_fecha_sap,
        id_zre, cod_naturaleza_juridica, naturaleza_juridica,
        anio, mes, id_usuario, fecha_distribucion
    )
    SELECT
        cod_matricula, max_fecha_plano, max_fecha_sap,
        id_zre, cod_naturaleza_juridica, naturaleza_juridica,
        anio, mes,
        usuarios_validos[((ROW_NUMBER() OVER ()) - 1) % total_usuarios + 1] AS id_usuario,
        CURRENT_DATE  -- se guarda la fecha actual
    FROM vw_compara_mutaciones;
END;
$$;


