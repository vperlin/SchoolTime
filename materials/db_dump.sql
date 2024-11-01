--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4 (Ubuntu 16.4-0ubuntu0.24.04.2)
-- Dumped by pg_dump version 16.4 (Ubuntu 16.4-0ubuntu0.24.04.2)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: _yoyo_log; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public._yoyo_log (
    id character varying(36) NOT NULL,
    migration_hash character varying(64),
    migration_id character varying(255),
    operation character varying(10),
    username character varying(255),
    hostname character varying(255),
    comment character varying(255),
    created_at_utc timestamp without time zone
);


ALTER TABLE public._yoyo_log OWNER TO admin;

--
-- Name: _yoyo_migration; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public._yoyo_migration (
    migration_hash character varying(64) NOT NULL,
    migration_id character varying(255),
    applied_at_utc timestamp without time zone
);


ALTER TABLE public._yoyo_migration OWNER TO admin;

--
-- Name: _yoyo_version; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public._yoyo_version (
    version integer NOT NULL,
    installed_at_utc timestamp without time zone
);


ALTER TABLE public._yoyo_version OWNER TO admin;

--
-- Name: metagroups; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.metagroups (
    iid integer NOT NULL,
    title text NOT NULL,
    note text
);


ALTER TABLE public.metagroups OWNER TO admin;

--
-- Name: metagroups_iid_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.metagroups_iid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.metagroups_iid_seq OWNER TO admin;

--
-- Name: metagroups_iid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.metagroups_iid_seq OWNED BY public.metagroups.iid;


--
-- Name: metagroups_students; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.metagroups_students (
    iid_metagroup integer NOT NULL,
    iid_student integer NOT NULL
);


ALTER TABLE public.metagroups_students OWNER TO admin;

--
-- Name: metagroups_subjects; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.metagroups_subjects (
    iid_metagroup integer NOT NULL,
    iid_subject integer NOT NULL
);


ALTER TABLE public.metagroups_subjects OWNER TO admin;

--
-- Name: sclasses; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.sclasses (
    iid integer NOT NULL,
    lyear integer NOT NULL,
    letter text,
    iid_leader integer,
    note text
);


ALTER TABLE public.sclasses OWNER TO admin;

--
-- Name: teachers; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.teachers (
    iid integer NOT NULL,
    last_name text NOT NULL,
    first_name text NOT NULL,
    middle_name text,
    phone text,
    note text,
    email text
);


ALTER TABLE public.teachers OWNER TO admin;

--
-- Name: sclass_info; Type: VIEW; Schema: public; Owner: admin
--

CREATE VIEW public.sclass_info AS
 SELECT cl.iid,
    cl.lyear,
    cl.letter,
    cl.iid_leader,
    cl.note,
    (((tc.last_name || ' '::text) || tc.first_name) || COALESCE((' '::text || tc.middle_name), ''::text)) AS name_leader,
    tc.phone AS leader_phones
   FROM (public.sclasses cl
     LEFT JOIN public.teachers tc ON ((cl.iid_leader = tc.iid)));


ALTER VIEW public.sclass_info OWNER TO admin;

--
-- Name: sclasses_iid_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.sclasses_iid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sclasses_iid_seq OWNER TO admin;

--
-- Name: sclasses_iid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.sclasses_iid_seq OWNED BY public.sclasses.iid;


--
-- Name: students; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.students (
    iid integer NOT NULL,
    last_name text NOT NULL,
    first_name text NOT NULL,
    middle_name text,
    phone text,
    phone_parents text,
    note text,
    iid_sclass integer NOT NULL
);


ALTER TABLE public.students OWNER TO admin;

--
-- Name: students_iid_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.students_iid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.students_iid_seq OWNER TO admin;

--
-- Name: students_iid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.students_iid_seq OWNED BY public.students.iid;


--
-- Name: subgroups; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.subgroups (
    iid integer NOT NULL,
    title text NOT NULL,
    iid_sclass integer NOT NULL,
    note text
);


ALTER TABLE public.subgroups OWNER TO admin;

--
-- Name: subgroups_iid_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.subgroups_iid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.subgroups_iid_seq OWNER TO admin;

--
-- Name: subgroups_iid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.subgroups_iid_seq OWNED BY public.subgroups.iid;


--
-- Name: subgroups_students; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.subgroups_students (
    iid_subgroup integer NOT NULL,
    iid_student integer NOT NULL
);


ALTER TABLE public.subgroups_students OWNER TO admin;

--
-- Name: subgroups_subjects; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.subgroups_subjects (
    iid_subgroup integer NOT NULL,
    iid_subject integer NOT NULL
);


ALTER TABLE public.subgroups_subjects OWNER TO admin;

--
-- Name: subjects; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.subjects (
    iid integer NOT NULL,
    code text NOT NULL,
    title text,
    note text
);


ALTER TABLE public.subjects OWNER TO admin;

--
-- Name: subjects_iid_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.subjects_iid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.subjects_iid_seq OWNER TO admin;

--
-- Name: subjects_iid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.subjects_iid_seq OWNED BY public.subjects.iid;


--
-- Name: teachers_iid_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.teachers_iid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.teachers_iid_seq OWNER TO admin;

--
-- Name: teachers_iid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.teachers_iid_seq OWNED BY public.teachers.iid;


--
-- Name: teachers_subjects; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.teachers_subjects (
    iid_teacher integer NOT NULL,
    iid_subject integer NOT NULL
);


ALTER TABLE public.teachers_subjects OWNER TO admin;

--
-- Name: teachers_info; Type: VIEW; Schema: public; Owner: admin
--

CREATE VIEW public.teachers_info AS
 WITH sbj AS (
         SELECT teachers_subjects.iid_teacher,
            array_agg(teachers_subjects.iid_subject) AS subjects
           FROM public.teachers_subjects
          GROUP BY teachers_subjects.iid_teacher
        )
 SELECT tc.iid,
    tc.last_name,
    tc.first_name,
    tc.middle_name,
    tc.phone,
    tc.note,
    COALESCE(sbj.subjects, ARRAY[]::integer[]) AS subjects,
    NULL::text AS lead_group
   FROM (public.teachers tc
     LEFT JOIN sbj ON ((sbj.iid_teacher = tc.iid)));


ALTER VIEW public.teachers_info OWNER TO admin;

--
-- Name: teachers_info1; Type: VIEW; Schema: public; Owner: admin
--

CREATE VIEW public.teachers_info1 AS
 WITH sbj AS (
         SELECT teachers_subjects.iid_teacher,
            array_agg(teachers_subjects.iid_subject) AS subjects
           FROM public.teachers_subjects
          GROUP BY teachers_subjects.iid_teacher
        )
 SELECT tc.iid,
    tc.last_name,
    tc.first_name,
    tc.middle_name,
    tc.phone,
    tc.email,
    tc.note,
    COALESCE(sbj.subjects, ARRAY[]::integer[]) AS subjects,
    NULL::text AS lead_group
   FROM (public.teachers tc
     LEFT JOIN sbj ON ((sbj.iid_teacher = tc.iid)));


ALTER VIEW public.teachers_info1 OWNER TO admin;

--
-- Name: yoyo_lock; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.yoyo_lock (
    locked integer DEFAULT 1 NOT NULL,
    ctime timestamp without time zone,
    pid integer NOT NULL
);


ALTER TABLE public.yoyo_lock OWNER TO admin;

--
-- Name: metagroups iid; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.metagroups ALTER COLUMN iid SET DEFAULT nextval('public.metagroups_iid_seq'::regclass);


--
-- Name: sclasses iid; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.sclasses ALTER COLUMN iid SET DEFAULT nextval('public.sclasses_iid_seq'::regclass);


--
-- Name: students iid; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.students ALTER COLUMN iid SET DEFAULT nextval('public.students_iid_seq'::regclass);


--
-- Name: subgroups iid; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subgroups ALTER COLUMN iid SET DEFAULT nextval('public.subgroups_iid_seq'::regclass);


--
-- Name: subjects iid; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects ALTER COLUMN iid SET DEFAULT nextval('public.subjects_iid_seq'::regclass);


--
-- Name: teachers iid; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.teachers ALTER COLUMN iid SET DEFAULT nextval('public.teachers_iid_seq'::regclass);


--
-- Data for Name: _yoyo_log; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public._yoyo_log (id, migration_hash, migration_id, operation, username, hostname, comment, created_at_utc) FROM stdin;
e8dab8f4-4a53-11ef-b5a1-9cda3e7798e0	70c569ba1e9f0d1ce56508c2f3beda0e8130a7eecb31805fbd553a3bad79729b	20240620_01_8gcUu-teachers-and-students	apply	vperlin	vplaptop	\N	2024-07-25 07:02:52.119208
e8dab8f5-4a53-11ef-b5a1-9cda3e7798e0	eb57ae8d3f719a68ef2ee2c13b6928a774cc2f9aaaef26538d2dd73102abfb4e	20240620_02_MKLUT-classes-and-subjects	apply	vperlin	vplaptop	\N	2024-07-25 07:02:52.611409
e8dab8f6-4a53-11ef-b5a1-9cda3e7798e0	18c57aaac6159975ccb022119f760a0bca5b0dc06231df6488f3dbacf890ac26	20240620_03_xGtkr-subgroups	apply	vperlin	vplaptop	\N	2024-07-25 07:02:53.236691
e8dab8f7-4a53-11ef-b5a1-9cda3e7798e0	a55ab9767af1972dfb42845f47d3c12de0559dbbb7225b3e6b3ac47c617340cf	20240711_01_QKBKV-permissions-for-subject-table	apply	vperlin	vplaptop	\N	2024-07-25 07:02:53.452806
53d57f2c-4e87-11ef-b5a1-c767530553af	1063630b436d482d166765145a9de511dfd85794f75bea9f35586e0a7ab0546c	20240730_01_EPRJ3-teachers-with-subjects	apply	vperlin	vplaptop	\N	2024-07-30 15:21:00.584581
5c680590-4e89-11ef-b5a1-c767530553af	1063630b436d482d166765145a9de511dfd85794f75bea9f35586e0a7ab0546c	20240730_01_EPRJ3-teachers-with-subjects	rollback	vperlin	vplaptop	\N	2024-07-30 15:35:33.964344
bed36d90-5268-11ef-b5a1-11a6971c198d	8944e8c0f529cc933023ac84b2eb1afaca9313c5ba132241a518247ce283160d	20240804_01_ViPpv-teachers-and-subjects	apply	vperlin	vplaptop	\N	2024-08-04 13:52:10.341976
c7c9f6bc-5268-11ef-b5a1-11a6971c198d	8944e8c0f529cc933023ac84b2eb1afaca9313c5ba132241a518247ce283160d	20240804_01_ViPpv-teachers-and-subjects	rollback	vperlin	vplaptop	\N	2024-08-04 13:52:25.380779
d9630968-5268-11ef-b5a1-11a6971c198d	8944e8c0f529cc933023ac84b2eb1afaca9313c5ba132241a518247ce283160d	20240804_01_ViPpv-teachers-and-subjects	apply	vperlin	vplaptop	\N	2024-08-04 13:52:54.903117
f93c9ccc-526d-11ef-b5a1-11a6971c198d	8944e8c0f529cc933023ac84b2eb1afaca9313c5ba132241a518247ce283160d	20240804_01_ViPpv-teachers-and-subjects	rollback	vperlin	vplaptop	\N	2024-08-04 14:29:35.8239
16c2de1e-526e-11ef-b5a1-11a6971c198d	8944e8c0f529cc933023ac84b2eb1afaca9313c5ba132241a518247ce283160d	20240804_01_ViPpv-teachers-and-subjects	apply	vperlin	vplaptop	\N	2024-08-04 14:30:25.359305
35201160-526e-11ef-b5a1-11a6971c198d	8944e8c0f529cc933023ac84b2eb1afaca9313c5ba132241a518247ce283160d	20240804_01_ViPpv-teachers-and-subjects	rollback	vperlin	vplaptop	\N	2024-08-04 14:31:16.298189
3a5da99e-526e-11ef-b5a1-11a6971c198d	8944e8c0f529cc933023ac84b2eb1afaca9313c5ba132241a518247ce283160d	20240804_01_ViPpv-teachers-and-subjects	apply	vperlin	vplaptop	\N	2024-08-04 14:31:25.090283
7c696bc6-5281-11ef-b5a1-11a6971c198d	f81920170d7fe08581b6948cdad6d5c3fc04a7eebbf69f87eb9967b3792235c9	20240804_02_rRiNc-adding-email-to-teacher	apply	vperlin	vplaptop	\N	2024-08-04 16:49:16.360687
c4c55ab0-5281-11ef-b5a1-11a6971c198d	48bb973ad6aba026b41c06f69f58dc0c9668e3e4ba2c22133b0b1ada4be54a7f	20240804_03_RyCJg-adding-emailto-teachers-info	apply	vperlin	vplaptop	\N	2024-08-04 16:51:17.733665
4d2c367a-5288-11ef-b5a1-11a6971c198d	9c890d89528b219581e2ddbd216259c1e6dddcf218275ae7eb4aa94aa11f82d1	20240804_04_gqWXd-correcting-subject-privileges	apply	vperlin	vplaptop	\N	2024-08-04 17:38:03.560963
750bd4c0-5288-11ef-b5a1-11a6971c198d	9c890d89528b219581e2ddbd216259c1e6dddcf218275ae7eb4aa94aa11f82d1	20240804_04_gqWXd-correcting-subject-privileges	rollback	vperlin	vplaptop	\N	2024-08-04 17:39:10.45516
b02322a2-5288-11ef-b5a1-11a6971c198d	9c890d89528b219581e2ddbd216259c1e6dddcf218275ae7eb4aa94aa11f82d1	20240804_04_gqWXd-correcting-subject-privileges	apply	vperlin	vplaptop	\N	2024-08-04 17:40:49.592689
fd05aa6c-83df-11ef-b5a1-9cda3e7798e0	9c890d89528b219581e2ddbd216259c1e6dddcf218275ae7eb4aa94aa11f82d1	20240804_04_gqWXd-correcting-subject-privileges	rollback	vperlin	vplaptop	\N	2024-10-06 12:39:11.775054
279870e8-83e0-11ef-b5a1-9cda3e7798e0	9c890d89528b219581e2ddbd216259c1e6dddcf218275ae7eb4aa94aa11f82d1	20240804_04_gqWXd-correcting-subject-privileges	apply	vperlin	vplaptop	\N	2024-10-06 12:40:23.20442
dd2039aa-83e0-11ef-b5a1-9cda3e7798e0	9c890d89528b219581e2ddbd216259c1e6dddcf218275ae7eb4aa94aa11f82d1	20240804_04_gqWXd-correcting-subject-privileges	rollback	vperlin	vplaptop	\N	2024-10-06 12:45:27.759184
e354e7c6-83e0-11ef-b5a1-9cda3e7798e0	9c890d89528b219581e2ddbd216259c1e6dddcf218275ae7eb4aa94aa11f82d1	20240804_04_gqWXd-correcting-subject-privileges	apply	vperlin	vplaptop	\N	2024-10-06 12:45:38.170281
9956cb1e-8988-11ef-b5a1-9cda3e7798e0	9c890d89528b219581e2ddbd216259c1e6dddcf218275ae7eb4aa94aa11f82d1	20240804_04_gqWXd-correcting-subject-privileges	rollback	vperlin	vplaptop	\N	2024-10-13 17:28:45.330715
af224720-8988-11ef-b5a1-9cda3e7798e0	9c890d89528b219581e2ddbd216259c1e6dddcf218275ae7eb4aa94aa11f82d1	20240804_04_gqWXd-correcting-subject-privileges	apply	vperlin	vplaptop	\N	2024-10-13 17:29:21.867195
dfc99788-8eca-11ef-b5a1-9cda3e7798e0	e40bb91894f9b0cdd6a7212c2d48e1b96f69b58a829c2c1417e1281c25306d3b	20241020_01_rOGSV-sclass-info	apply	vperlin	vplaptop	\N	2024-10-20 10:05:46.115351
97d11360-8ecb-11ef-b5a1-9cda3e7798e0	e40bb91894f9b0cdd6a7212c2d48e1b96f69b58a829c2c1417e1281c25306d3b	20241020_01_rOGSV-sclass-info	rollback	vperlin	vplaptop	\N	2024-10-20 10:10:54.840682
9d01c7a8-8ecb-11ef-b5a1-9cda3e7798e0	e40bb91894f9b0cdd6a7212c2d48e1b96f69b58a829c2c1417e1281c25306d3b	20241020_01_rOGSV-sclass-info	apply	vperlin	vplaptop	\N	2024-10-20 10:11:03.544291
ab99baee-8edc-11ef-b5a1-9cda3e7798e0	e40bb91894f9b0cdd6a7212c2d48e1b96f69b58a829c2c1417e1281c25306d3b	20241020_01_rOGSV-sclass-info	rollback	vperlin	vplaptop	\N	2024-10-20 12:13:09.472482
ab99baef-8edc-11ef-b5a1-9cda3e7798e0	9c890d89528b219581e2ddbd216259c1e6dddcf218275ae7eb4aa94aa11f82d1	20240804_04_gqWXd-correcting-subject-privileges	rollback	vperlin	vplaptop	\N	2024-10-20 12:13:09.62759
af941b12-8edc-11ef-b5a1-9cda3e7798e0	9c890d89528b219581e2ddbd216259c1e6dddcf218275ae7eb4aa94aa11f82d1	20240804_04_gqWXd-correcting-subject-privileges	apply	vperlin	vplaptop	\N	2024-10-20 12:13:16.146946
af941b13-8edc-11ef-b5a1-9cda3e7798e0	e40bb91894f9b0cdd6a7212c2d48e1b96f69b58a829c2c1417e1281c25306d3b	20241020_01_rOGSV-sclass-info	apply	vperlin	vplaptop	\N	2024-10-20 12:13:16.302533
be00bffc-8edc-11ef-b5a1-9cda3e7798e0	e40bb91894f9b0cdd6a7212c2d48e1b96f69b58a829c2c1417e1281c25306d3b	20241020_01_rOGSV-sclass-info	rollback	vperlin	vplaptop	\N	2024-10-20 12:13:40.348781
be00bffd-8edc-11ef-b5a1-9cda3e7798e0	9c890d89528b219581e2ddbd216259c1e6dddcf218275ae7eb4aa94aa11f82d1	20240804_04_gqWXd-correcting-subject-privileges	rollback	vperlin	vplaptop	\N	2024-10-20 12:13:40.60424
c21a3dc0-8edc-11ef-b5a1-9cda3e7798e0	9c890d89528b219581e2ddbd216259c1e6dddcf218275ae7eb4aa94aa11f82d1	20240804_04_gqWXd-correcting-subject-privileges	apply	vperlin	vplaptop	\N	2024-10-20 12:13:47.226187
c21a3dc1-8edc-11ef-b5a1-9cda3e7798e0	e40bb91894f9b0cdd6a7212c2d48e1b96f69b58a829c2c1417e1281c25306d3b	20241020_01_rOGSV-sclass-info	apply	vperlin	vplaptop	\N	2024-10-20 12:13:47.471443
\.


--
-- Data for Name: _yoyo_migration; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public._yoyo_migration (migration_hash, migration_id, applied_at_utc) FROM stdin;
70c569ba1e9f0d1ce56508c2f3beda0e8130a7eecb31805fbd553a3bad79729b	20240620_01_8gcUu-teachers-and-students	2024-07-25 07:02:52.17067
eb57ae8d3f719a68ef2ee2c13b6928a774cc2f9aaaef26538d2dd73102abfb4e	20240620_02_MKLUT-classes-and-subjects	2024-07-25 07:02:52.652475
18c57aaac6159975ccb022119f760a0bca5b0dc06231df6488f3dbacf890ac26	20240620_03_xGtkr-subgroups	2024-07-25 07:02:53.27838
a55ab9767af1972dfb42845f47d3c12de0559dbbb7225b3e6b3ac47c617340cf	20240711_01_QKBKV-permissions-for-subject-table	2024-07-25 07:02:53.494547
8944e8c0f529cc933023ac84b2eb1afaca9313c5ba132241a518247ce283160d	20240804_01_ViPpv-teachers-and-subjects	2024-08-04 14:31:25.132231
f81920170d7fe08581b6948cdad6d5c3fc04a7eebbf69f87eb9967b3792235c9	20240804_02_rRiNc-adding-email-to-teacher	2024-08-04 16:49:16.435305
48bb973ad6aba026b41c06f69f58dc0c9668e3e4ba2c22133b0b1ada4be54a7f	20240804_03_RyCJg-adding-emailto-teachers-info	2024-08-04 16:51:17.777752
9c890d89528b219581e2ddbd216259c1e6dddcf218275ae7eb4aa94aa11f82d1	20240804_04_gqWXd-correcting-subject-privileges	2024-10-20 12:13:47.30891
e40bb91894f9b0cdd6a7212c2d48e1b96f69b58a829c2c1417e1281c25306d3b	20241020_01_rOGSV-sclass-info	2024-10-20 12:13:47.514624
\.


--
-- Data for Name: _yoyo_version; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public._yoyo_version (version, installed_at_utc) FROM stdin;
2	2024-07-25 07:02:44.313251
\.


--
-- Data for Name: metagroups; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.metagroups (iid, title, note) FROM stdin;
\.


--
-- Data for Name: metagroups_students; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.metagroups_students (iid_metagroup, iid_student) FROM stdin;
\.


--
-- Data for Name: metagroups_subjects; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.metagroups_subjects (iid_metagroup, iid_subject) FROM stdin;
\.


--
-- Data for Name: sclasses; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.sclasses (iid, lyear, letter, iid_leader, note) FROM stdin;
1	8	а	111	\N
2	8	б	110	\N
3	10	a	117	\N
4	11	б	118	\N
\.


--
-- Data for Name: students; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.students (iid, last_name, first_name, middle_name, phone, phone_parents, note, iid_sclass) FROM stdin;
3	Иванов	Иван	Иванович		\N	\N	1
4	Петров	Петр	Петрович	\N	\N	\N	1
5	Сидоров	Сидор	Сидорович	\N	\N	\N	2
\.


--
-- Data for Name: subgroups; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.subgroups (iid, title, iid_sclass, note) FROM stdin;
1	1	1	\N
2	2	1	\N
3	1	2	\N
4	2	2	\N
5	3	2	\N
6	1	3	\N
7	1	4	\N
8	2	4	\N
\.


--
-- Data for Name: subgroups_students; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.subgroups_students (iid_subgroup, iid_student) FROM stdin;
1	3
2	4
3	5
\.


--
-- Data for Name: subgroups_subjects; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.subgroups_subjects (iid_subgroup, iid_subject) FROM stdin;
\.


--
-- Data for Name: subjects; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.subjects (iid, code, title, note) FROM stdin;
1	рус	\N	\N
2	англ	\N	\N
3	мат	\N	\N
4	физ	\N	\N
6	геогр	\N	\N
7	биол	\N	\N
8	шахм	\N	\N
9	физра	\N	\N
10	общ	\N	\N
11	ист	\N	\N
12	лит	\N	\N
13	проект	\N	\N
14	техн	\N	\N
15	инф	\N	\N
16	нем	\N	\N
17	фарси	\N	\N
\.


--
-- Data for Name: teachers; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.teachers (iid, last_name, first_name, middle_name, phone, note, email) FROM stdin;
109	Попугайчиков	Флегонт	Егорович	+7(111)222-33-44	\N	popka123@list.ru
110	Сидоров	Антиох	Елпидифорович	+7(216)126-09-56	\N	sidoroff@mail.ru
111	Брандахлыстова	Людмила	Петровна	+7(892)098-12-34	\N	branda@yandex.ru
112	Рабин	Георгий	Аланович	+7(672)958-30-63	\N	rtcucs@yandex.ru
113	Егорновa	Каролина	Эллиотовна	+7(633)594-80-44	\N	lwbmbba@list.ru
114	Балабановa	Настасия	Климентовна	+7(646)959-63-32	\N	lfplheya@yandex.ru
115	Неустроев	Харрисон	Публиевич	+7(415)188-88-78	\N	dyqvfmx@yandex.ru
116	Чевыкинa	Консуэлла	Хильдериковна	+7(586)541-79-52	\N	vunyeueen@list.ru
117	Элевертов	Кристиан	Даниилович	+7(390)181-88-77	\N	dract@yandex.ru
118	Феденко	Фессалоникия	Эразмовна	+7(583)368-67-80	\N	siproxkm@yandex.ru
119	Губанов	Альвиз	Савельевич	+7(811)131-74-99	\N	qjenzxwk@rambler.ru
120	Асташев	Алон	Рейнхардович	+7(414)048-33-12	\N	ozsllc@yandex.ru
121	Хрущев	Фарид	Геронтиевич	+7(124)622-82-50	\N	wtckqqlr@mail.ru
122	Кострецовa	Леда	Гельмутовна	+7(618)043-87-16	\N	wkehhaqvg@list.ru
123	Онохинa	Валентина	Рагуиловна	+7(105)206-07-85	\N	osevsx@mail.ru
124	Евграновa	Тина	Кадваллоновна	+7(383)037-14-35	\N	idgnm@mail.ru
125	Бузуновa	Аксинья	Святославовна	+7(253)051-18-58	\N	beabml@list.ru
126	Арестовa	Каролина	Октавиевна	+7(119)956-48-26	\N	qdbgv@post.ru
127	Яцких	Селина	Хильдериковна	+7(649)316-29-95	\N	kxrhmrgns@list.ru
128	Уткин	Эдна	Викторович	+7(731)264-64-86	\N	mxdom@list.ru
129	Базырин	Тихомир	Викторович	+7(631)561-03-82	\N	rzcbd@list.ru
130	Воронцовa	Бланка	Кадировна	+7(330)840-65-78	\N	hrzyzxh@rambler.ru
131	Ященко	Земфира	Клавдиановна	+7(147)362-84-48	\N	uvsxe@mail.ru
132	Днепровская	Кикилия	Касьяновна	+7(263)656-96-24	\N	awmdvmwo@post.ru
133	Кривощаповa	Каллисфения	Савватиевна	+7(309)319-42-47	\N	ugoyhz@post.ru
134	Ожгихин	Герман	Корнилиевич	+7(770)908-17-15	\N	bfpuoalz@yandex.ru
135	Амеличев	Ландульф	Альбинович	+7(307)224-90-18	\N	tvphieerk@list.ru
136	Галикарнакская	Марина	Конрадовна	+7(211)553-42-59	\N	msmdfqwr@yandex.ru
137	Раздобаринa	Денница	Васильевна	+7(867)096-80-12	\N	abjhq@post.ru
138	Буланый	Абид	Семёнович	+7(562)274-85-55	\N	xhkbbju@mail.ru
139	Степчевa	Агафоника	Лавсовна	+7(269)231-65-65	\N	rfrlwia@mail.ru
140	Колюхинa	Горислава	Османовна	+7(863)675-15-80	\N	feawcq@rambler.ru
141	Постельников	Аркадий	Илларионович	+7(474)868-26-80	\N	klomcutfa@post.ru
142	Скоробогатовa	Филарета	Линкеевна	+7(053)253-79-89	\N	uulxmfo@list.ru
143	Коженко	Алфея	Иродионовна	+7(266)065-08-99	\N	vufrgpdo@yandex.ru
144	Подлекаревa	Флорентина	Золтановна	+7(822)432-85-93	\N	mybxh@yandex.ru
145	Павлюковецa	Клеопатра	Зиноновна	+7(605)855-14-97	\N	dpogywb@post.ru
146	Бархоткин	Октавий	Бертович	+7(161)929-83-30	\N	ntbhgae@list.ru
147	Бачуринская	Тахмина	Джоновна	+7(812)468-05-32	\N	ayflot@post.ru
148	Гудаевa	Ноэми	Эберхардовна	+7(857)130-91-30	\N	mgxbuu@rambler.ru
149	Гурилёвa	Ядвига	Адилевна	+7(943)818-76-57	\N	vpshitfve@post.ru
150	Иоселович	Магдалина	Гордеевна	+7(867)580-63-98	\N	wvwcnij@list.ru
151	Калининская	Заира	Кимовна	+7(921)502-81-51	\N	inorsitv@rambler.ru
152	Боташевa	Азелла	Леонхардовна	+7(439)429-61-74	\N	ymhnrthi@mail.ru
153	Фиговский	Иосафат	Зиeвич	+7(541)921-35-80	\N	qnlywxal@post.ru
154	Французовa	Модеста	Мурадовна	+7(063)688-37-11	\N	vbrhn@list.ru
155	Гусляровa	Олеся	Несторовна	+7(006)856-32-44	\N	ksodvddk@post.ru
156	Мартышковa	Марионелла	Володарьевна	+7(302)162-48-32	\N	dqowazyeh@mail.ru
157	Гоглачевa	Дарина	Септимиевна	+7(584)323-83-11	\N	ekkcytn@mail.ru
158	Ромашихин	Киллиан	Емельянович	+7(468)085-05-28	\N	qdwzosm@rambler.ru
159	Космач	Бартоломео	Федотович	+7(893)352-86-79	\N	knsjsgnl@mail.ru
160	Павлюченковa	Валия	Артуровна	+7(796)782-15-85	\N	munkhcdz@rambler.ru
\.


--
-- Data for Name: teachers_subjects; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.teachers_subjects (iid_teacher, iid_subject) FROM stdin;
109	6
112	7
113	7
114	4
115	4
116	4
117	4
118	8
120	9
121	9
122	9
125	9
127	11
127	10
128	11
128	10
129	11
129	10
130	11
130	10
131	11
131	10
132	1
132	12
133	1
133	12
134	1
134	12
135	1
135	12
136	1
136	12
137	1
137	12
138	3
139	3
140	3
141	3
142	3
143	3
144	3
145	3
146	3
147	3
148	15
148	14
149	15
149	14
150	15
151	15
151	13
152	15
152	14
152	13
152	3
153	15
153	14
153	13
154	2
155	2
156	2
157	2
157	16
158	2
158	16
159	2
159	17
160	2
\.


--
-- Data for Name: yoyo_lock; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.yoyo_lock (locked, ctime, pid) FROM stdin;
\.


--
-- Name: metagroups_iid_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.metagroups_iid_seq', 1, false);


--
-- Name: sclasses_iid_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.sclasses_iid_seq', 4, true);


--
-- Name: students_iid_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.students_iid_seq', 5, true);


--
-- Name: subgroups_iid_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.subgroups_iid_seq', 8, true);


--
-- Name: subjects_iid_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.subjects_iid_seq', 17, true);


--
-- Name: teachers_iid_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.teachers_iid_seq', 160, true);


--
-- Name: _yoyo_log _yoyo_log_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public._yoyo_log
    ADD CONSTRAINT _yoyo_log_pkey PRIMARY KEY (id);


--
-- Name: _yoyo_migration _yoyo_migration_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public._yoyo_migration
    ADD CONSTRAINT _yoyo_migration_pkey PRIMARY KEY (migration_hash);


--
-- Name: _yoyo_version _yoyo_version_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public._yoyo_version
    ADD CONSTRAINT _yoyo_version_pkey PRIMARY KEY (version);


--
-- Name: metagroups metagroups_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.metagroups
    ADD CONSTRAINT metagroups_pkey PRIMARY KEY (iid);


--
-- Name: metagroups_students metagroups_students_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.metagroups_students
    ADD CONSTRAINT metagroups_students_pkey PRIMARY KEY (iid_metagroup, iid_student);


--
-- Name: metagroups_subjects metagroups_subjects_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.metagroups_subjects
    ADD CONSTRAINT metagroups_subjects_pkey PRIMARY KEY (iid_metagroup, iid_subject);


--
-- Name: sclasses sclasses_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.sclasses
    ADD CONSTRAINT sclasses_pkey PRIMARY KEY (iid);


--
-- Name: students students_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_pkey PRIMARY KEY (iid);


--
-- Name: subgroups subgroups_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subgroups
    ADD CONSTRAINT subgroups_pkey PRIMARY KEY (iid);


--
-- Name: subgroups_students subgroups_students_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subgroups_students
    ADD CONSTRAINT subgroups_students_pkey PRIMARY KEY (iid_subgroup, iid_student);


--
-- Name: subgroups_subjects subgroups_subjects_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subgroups_subjects
    ADD CONSTRAINT subgroups_subjects_pkey PRIMARY KEY (iid_subgroup, iid_subject);


--
-- Name: subjects subjects_code_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects
    ADD CONSTRAINT subjects_code_key UNIQUE (code);


--
-- Name: subjects subjects_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects
    ADD CONSTRAINT subjects_pkey PRIMARY KEY (iid);


--
-- Name: teachers teachers_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.teachers
    ADD CONSTRAINT teachers_pkey PRIMARY KEY (iid);


--
-- Name: teachers_subjects teachers_subjects_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.teachers_subjects
    ADD CONSTRAINT teachers_subjects_pkey PRIMARY KEY (iid_teacher, iid_subject);


--
-- Name: yoyo_lock yoyo_lock_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.yoyo_lock
    ADD CONSTRAINT yoyo_lock_pkey PRIMARY KEY (locked);


--
-- Name: metagroups_students metagroups_students_iid_metagroup_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.metagroups_students
    ADD CONSTRAINT metagroups_students_iid_metagroup_fkey FOREIGN KEY (iid_metagroup) REFERENCES public.metagroups(iid);


--
-- Name: metagroups_students metagroups_students_iid_student_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.metagroups_students
    ADD CONSTRAINT metagroups_students_iid_student_fkey FOREIGN KEY (iid_student) REFERENCES public.students(iid);


--
-- Name: metagroups_subjects metagroups_subjects_iid_metagroup_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.metagroups_subjects
    ADD CONSTRAINT metagroups_subjects_iid_metagroup_fkey FOREIGN KEY (iid_metagroup) REFERENCES public.metagroups(iid);


--
-- Name: metagroups_subjects metagroups_subjects_iid_subject_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.metagroups_subjects
    ADD CONSTRAINT metagroups_subjects_iid_subject_fkey FOREIGN KEY (iid_subject) REFERENCES public.subjects(iid);


--
-- Name: sclasses sclasses_iid_leader_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.sclasses
    ADD CONSTRAINT sclasses_iid_leader_fkey FOREIGN KEY (iid_leader) REFERENCES public.teachers(iid);


--
-- Name: students students_iid_sclass_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_iid_sclass_fkey FOREIGN KEY (iid_sclass) REFERENCES public.sclasses(iid);


--
-- Name: subgroups subgroups_iid_sclass_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subgroups
    ADD CONSTRAINT subgroups_iid_sclass_fkey FOREIGN KEY (iid_sclass) REFERENCES public.sclasses(iid);


--
-- Name: subgroups_students subgroups_students_iid_student_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subgroups_students
    ADD CONSTRAINT subgroups_students_iid_student_fkey FOREIGN KEY (iid_student) REFERENCES public.students(iid);


--
-- Name: subgroups_students subgroups_students_iid_subgroup_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subgroups_students
    ADD CONSTRAINT subgroups_students_iid_subgroup_fkey FOREIGN KEY (iid_subgroup) REFERENCES public.subgroups(iid);


--
-- Name: subgroups_subjects subgroups_subjects_iid_subgroup_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subgroups_subjects
    ADD CONSTRAINT subgroups_subjects_iid_subgroup_fkey FOREIGN KEY (iid_subgroup) REFERENCES public.subgroups(iid);


--
-- Name: subgroups_subjects subgroups_subjects_iid_subject_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subgroups_subjects
    ADD CONSTRAINT subgroups_subjects_iid_subject_fkey FOREIGN KEY (iid_subject) REFERENCES public.subjects(iid);


--
-- Name: teachers_subjects teachers_subjects_iid_subject_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.teachers_subjects
    ADD CONSTRAINT teachers_subjects_iid_subject_fkey FOREIGN KEY (iid_subject) REFERENCES public.subjects(iid);


--
-- Name: teachers_subjects teachers_subjects_iid_teacher_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.teachers_subjects
    ADD CONSTRAINT teachers_subjects_iid_teacher_fkey FOREIGN KEY (iid_teacher) REFERENCES public.teachers(iid);


--
-- Name: TABLE sclasses; Type: ACL; Schema: public; Owner: admin
--

GRANT SELECT,INSERT,UPDATE ON TABLE public.sclasses TO PUBLIC;


--
-- Name: TABLE teachers; Type: ACL; Schema: public; Owner: admin
--

GRANT SELECT,INSERT,UPDATE ON TABLE public.teachers TO PUBLIC;


--
-- Name: TABLE sclass_info; Type: ACL; Schema: public; Owner: admin
--

GRANT SELECT ON TABLE public.sclass_info TO PUBLIC;


--
-- Name: SEQUENCE sclasses_iid_seq; Type: ACL; Schema: public; Owner: admin
--

GRANT USAGE ON SEQUENCE public.sclasses_iid_seq TO PUBLIC;


--
-- Name: TABLE students; Type: ACL; Schema: public; Owner: admin
--

GRANT SELECT,INSERT,UPDATE ON TABLE public.students TO PUBLIC;


--
-- Name: SEQUENCE students_iid_seq; Type: ACL; Schema: public; Owner: admin
--

GRANT USAGE ON SEQUENCE public.students_iid_seq TO PUBLIC;


--
-- Name: TABLE subjects; Type: ACL; Schema: public; Owner: admin
--

GRANT SELECT,INSERT,UPDATE ON TABLE public.subjects TO PUBLIC;


--
-- Name: SEQUENCE subjects_iid_seq; Type: ACL; Schema: public; Owner: admin
--

GRANT USAGE ON SEQUENCE public.subjects_iid_seq TO PUBLIC;


--
-- Name: SEQUENCE teachers_iid_seq; Type: ACL; Schema: public; Owner: admin
--

GRANT USAGE ON SEQUENCE public.teachers_iid_seq TO PUBLIC;


--
-- Name: TABLE teachers_subjects; Type: ACL; Schema: public; Owner: admin
--

GRANT INSERT,DELETE ON TABLE public.teachers_subjects TO PUBLIC;


--
-- Name: TABLE teachers_info; Type: ACL; Schema: public; Owner: admin
--

GRANT SELECT ON TABLE public.teachers_info TO PUBLIC;


--
-- Name: TABLE teachers_info1; Type: ACL; Schema: public; Owner: admin
--

GRANT SELECT ON TABLE public.teachers_info1 TO PUBLIC;


--
-- PostgreSQL database dump complete
--

