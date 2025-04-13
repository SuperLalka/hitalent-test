--
-- PostgreSQL database dump
--

-- Dumped from database version 16.8 (Debian 16.8-1.pgdg120+1)
-- Dumped by pg_dump version 16.8 (Debian 16.8-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- ALTER TABLE ONLY public.reservation DROP CONSTRAINT reservation_table_id_fkey;
-- DROP INDEX public.ix_reservation_table_id;
-- ALTER TABLE ONLY public."table" DROP CONSTRAINT table_pkey;
-- ALTER TABLE ONLY public.reservation DROP CONSTRAINT reservation_pkey;
-- ALTER TABLE ONLY public.alembic_version DROP CONSTRAINT alembic_version_pkc;
-- ALTER TABLE public."table" ALTER COLUMN id DROP DEFAULT;
-- DROP SEQUENCE public.table_id_seq;
-- DROP TABLE public."table";
-- DROP TABLE public.reservation;
-- DROP TABLE public.alembic_version;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: debug
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO debug;

--
-- Name: reservation; Type: TABLE; Schema: public; Owner: debug
--

CREATE TABLE public.reservation (
    id uuid NOT NULL,
    customer_name character varying NOT NULL,
    reservation_time timestamp without time zone,
    duration_minutes integer NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    table_id bigint NOT NULL
);


ALTER TABLE public.reservation OWNER TO debug;

--
-- Name: table; Type: TABLE; Schema: public; Owner: debug
--

CREATE TABLE public."table" (
    id bigint NOT NULL,
    name character varying(50) NOT NULL,
    seats integer NOT NULL,
    location character varying(50),
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public."table" OWNER TO debug;

--
-- Name: table_id_seq; Type: SEQUENCE; Schema: public; Owner: debug
--

CREATE SEQUENCE public.table_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.table_id_seq OWNER TO debug;

--
-- Name: table_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: debug
--

ALTER SEQUENCE public.table_id_seq OWNED BY public."table".id;


--
-- Name: table id; Type: DEFAULT; Schema: public; Owner: debug
--

ALTER TABLE ONLY public."table" ALTER COLUMN id SET DEFAULT nextval('public.table_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: debug
--

COPY public.alembic_version (version_num) FROM stdin;
1b89263ee7b0
\.


--
-- Data for Name: reservation; Type: TABLE DATA; Schema: public; Owner: debug
--

COPY public.reservation (id, customer_name, reservation_time, duration_minutes, created_at, updated_at, table_id) FROM stdin;
19a6d22b-43f4-4b86-b711-1436f442217f	Иван Иванов	2025-04-20 10:00:00	60	2025-04-13 08:04:16.635819	2025-04-13 08:04:16.635819	1
19a3f123-aca5-428b-9d95-34baf6266e75	Петр Петров	2025-04-20 11:01:00	120	2025-04-13 08:06:47.402922	2025-04-13 08:06:47.402922	1
\.


--
-- Data for Name: table; Type: TABLE DATA; Schema: public; Owner: debug
--

COPY public."table" (id, name, seats, location, created_at, updated_at) FROM stdin;
1	Парный 1	2	основной зал	2025-04-10 17:56:38.498513	2025-04-10 17:56:38.498513
2	Парный 2	2	основной зал	2025-04-10 18:15:11.026251	2025-04-10 18:15:11.026251
3	Парный 3	2	терраса	2025-04-10 18:16:22.060605	2025-04-10 18:16:22.060605
4	Парный 4	2	терраса	2025-04-10 18:16:37.947787	2025-04-10 18:16:37.947787
5	Групповой 1	4	основной зал	2025-04-10 18:20:25.615284	2025-04-10 18:20:25.615284
6	Групповой 2	4	основной зал	2025-04-10 18:20:41.737216	2025-04-10 18:20:41.737216
7	Групповой 3	4	терраса	2025-04-10 18:21:08.687806	2025-04-10 18:21:08.687806
8	Групповой 1Б	8	компанейский зал 1	2025-04-10 18:21:43.691816	2025-04-10 18:21:43.691816
9	Групповой 2Б	8	компанейский зал 2	2025-04-10 18:24:05.228126	2025-04-10 18:24:05.228126
10	Конференц	12	деловой зал	2025-04-10 18:24:14.148324	2025-04-10 18:24:14.148324
\.


--
-- Name: table_id_seq; Type: SEQUENCE SET; Schema: public; Owner: debug
--

SELECT pg_catalog.setval('public.table_id_seq', 13, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: debug
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: reservation reservation_pkey; Type: CONSTRAINT; Schema: public; Owner: debug
--

ALTER TABLE ONLY public.reservation
    ADD CONSTRAINT reservation_pkey PRIMARY KEY (id);


--
-- Name: table table_pkey; Type: CONSTRAINT; Schema: public; Owner: debug
--

ALTER TABLE ONLY public."table"
    ADD CONSTRAINT table_pkey PRIMARY KEY (id);


--
-- Name: ix_reservation_table_id; Type: INDEX; Schema: public; Owner: debug
--

CREATE INDEX ix_reservation_table_id ON public.reservation USING btree (table_id);


--
-- Name: reservation reservation_table_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: debug
--

ALTER TABLE ONLY public.reservation
    ADD CONSTRAINT reservation_table_id_fkey FOREIGN KEY (table_id) REFERENCES public."table"(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

