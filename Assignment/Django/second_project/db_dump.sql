--
-- PostgreSQL database dump
--

\restrict maHUPDRwfzAVTX7EJIWH0hRbTZmgJxNsdiDVolrnUzWe2Y25sVNusVFId8qQh2a

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id;
ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co;
ALTER TABLE ONLY public.cine_verse_watchhistory DROP CONSTRAINT cine_verse_watchhistory_user_id_68f3f5d3_fk_auth_user_id;
ALTER TABLE ONLY public.cine_verse_watchhistory DROP CONSTRAINT cine_verse_watchhist_movie_id_a6d3ccb0_fk_cine_vers;
ALTER TABLE ONLY public.cine_verse_userprofile DROP CONSTRAINT cine_verse_userprofile_user_id_a771f7ab_fk_auth_user_id;
ALTER TABLE ONLY public.cine_verse_userprofile_favorite_genres DROP CONSTRAINT cine_verse_userprofi_userprofile_id_c87cacd0_fk_cine_vers;
ALTER TABLE ONLY public.cine_verse_userprofile_favorites DROP CONSTRAINT cine_verse_userprofi_userprofile_id_91062bbf_fk_cine_vers;
ALTER TABLE ONLY public.cine_verse_userprofile_watchlist DROP CONSTRAINT cine_verse_userprofi_userprofile_id_87ccd15e_fk_cine_vers;
ALTER TABLE ONLY public.cine_verse_userprofile_watchlist DROP CONSTRAINT cine_verse_userprofi_movie_id_e2741fdf_fk_cine_vers;
ALTER TABLE ONLY public.cine_verse_userprofile_favorites DROP CONSTRAINT cine_verse_userprofi_movie_id_ab61c4f1_fk_cine_vers;
ALTER TABLE ONLY public.cine_verse_userprofile_favorite_genres DROP CONSTRAINT cine_verse_userprofi_genre_id_eafe4b19_fk_cine_vers;
ALTER TABLE ONLY public.cine_verse_movie_genres DROP CONSTRAINT cine_verse_movie_gen_movie_id_93858df4_fk_cine_vers;
ALTER TABLE ONLY public.cine_verse_movie_genres DROP CONSTRAINT cine_verse_movie_gen_genre_id_b380ec4e_fk_cine_vers;
ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id;
ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm;
ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id;
ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
DROP INDEX public.django_session_session_key_c0390e0f_like;
DROP INDEX public.django_session_expire_date_a5c62663;
DROP INDEX public.django_admin_log_user_id_c564eba6;
DROP INDEX public.django_admin_log_content_type_id_c4bce8eb;
DROP INDEX public.cine_verse_watchhistory_user_id_68f3f5d3;
DROP INDEX public.cine_verse_watchhistory_movie_id_a6d3ccb0;
DROP INDEX public.cine_verse_userprofile_watchlist_userprofile_id_87ccd15e;
DROP INDEX public.cine_verse_userprofile_watchlist_movie_id_e2741fdf;
DROP INDEX public.cine_verse_userprofile_favorites_userprofile_id_91062bbf;
DROP INDEX public.cine_verse_userprofile_favorites_movie_id_ab61c4f1;
DROP INDEX public.cine_verse_userprofile_favorite_genres_userprofile_id_c87cacd0;
DROP INDEX public.cine_verse_userprofile_favorite_genres_genre_id_eafe4b19;
DROP INDEX public.cine_verse_movie_genres_movie_id_93858df4;
DROP INDEX public.cine_verse_movie_genres_genre_id_b380ec4e;
DROP INDEX public.cine_verse_genre_slug_86cbb62f_like;
DROP INDEX public.auth_user_username_6821ab7c_like;
DROP INDEX public.auth_user_user_permissions_user_id_a95ead1b;
DROP INDEX public.auth_user_user_permissions_permission_id_1fbb5f2c;
DROP INDEX public.auth_user_groups_user_id_6a12ed8b;
DROP INDEX public.auth_user_groups_group_id_97559544;
DROP INDEX public.auth_permission_content_type_id_2f476e4b;
DROP INDEX public.auth_group_permissions_permission_id_84c5c92e;
DROP INDEX public.auth_group_permissions_group_id_b120cbf9;
DROP INDEX public.auth_group_name_a6ea08ec_like;
ALTER TABLE ONLY public.django_session DROP CONSTRAINT django_session_pkey;
ALTER TABLE ONLY public.django_migrations DROP CONSTRAINT django_migrations_pkey;
ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_pkey;
ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq;
ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_pkey;
ALTER TABLE ONLY public.cine_verse_watchhistory DROP CONSTRAINT cine_verse_watchhistory_user_id_movie_id_e7bc2c96_uniq;
ALTER TABLE ONLY public.cine_verse_watchhistory DROP CONSTRAINT cine_verse_watchhistory_pkey;
ALTER TABLE ONLY public.cine_verse_userprofile_watchlist DROP CONSTRAINT cine_verse_userprofile_watchlist_pkey;
ALTER TABLE ONLY public.cine_verse_userprofile_watchlist DROP CONSTRAINT cine_verse_userprofile_w_userprofile_id_movie_id_fba4c27a_uniq;
ALTER TABLE ONLY public.cine_verse_userprofile DROP CONSTRAINT cine_verse_userprofile_user_id_key;
ALTER TABLE ONLY public.cine_verse_userprofile DROP CONSTRAINT cine_verse_userprofile_pkey;
ALTER TABLE ONLY public.cine_verse_userprofile_favorites DROP CONSTRAINT cine_verse_userprofile_favorites_pkey;
ALTER TABLE ONLY public.cine_verse_userprofile_favorite_genres DROP CONSTRAINT cine_verse_userprofile_favorite_genres_pkey;
ALTER TABLE ONLY public.cine_verse_userprofile_favorites DROP CONSTRAINT cine_verse_userprofile_f_userprofile_id_movie_id_ef889f9b_uniq;
ALTER TABLE ONLY public.cine_verse_userprofile_favorite_genres DROP CONSTRAINT cine_verse_userprofile_f_userprofile_id_genre_id_5bdbe273_uniq;
ALTER TABLE ONLY public.cine_verse_movie DROP CONSTRAINT cine_verse_movie_pkey;
ALTER TABLE ONLY public.cine_verse_movie_genres DROP CONSTRAINT cine_verse_movie_genres_pkey;
ALTER TABLE ONLY public.cine_verse_movie_genres DROP CONSTRAINT cine_verse_movie_genres_movie_id_genre_id_949ee331_uniq;
ALTER TABLE ONLY public.cine_verse_genre DROP CONSTRAINT cine_verse_genre_slug_key;
ALTER TABLE ONLY public.cine_verse_genre DROP CONSTRAINT cine_verse_genre_pkey;
ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_username_key;
ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq;
ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_pkey;
ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_pkey;
ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq;
ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_pkey;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_pkey;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq;
ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_pkey;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_pkey;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_name_key;
DROP TABLE public.django_session;
DROP TABLE public.django_migrations;
DROP TABLE public.django_content_type;
DROP TABLE public.django_admin_log;
DROP TABLE public.cine_verse_watchhistory;
DROP TABLE public.cine_verse_userprofile_watchlist;
DROP TABLE public.cine_verse_userprofile_favorites;
DROP TABLE public.cine_verse_userprofile_favorite_genres;
DROP TABLE public.cine_verse_userprofile;
DROP TABLE public.cine_verse_movie_genres;
DROP TABLE public.cine_verse_movie;
DROP TABLE public.cine_verse_genre;
DROP TABLE public.auth_user_user_permissions;
DROP TABLE public.auth_user_groups;
DROP TABLE public.auth_user;
DROP TABLE public.auth_permission;
DROP TABLE public.auth_group_permissions;
DROP TABLE public.auth_group;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_user_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_user ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: cine_verse_genre; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cine_verse_genre (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    slug character varying(50) NOT NULL
);


--
-- Name: cine_verse_genre_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.cine_verse_genre ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.cine_verse_genre_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: cine_verse_movie; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cine_verse_movie (
    id bigint NOT NULL,
    title character varying(255) NOT NULL,
    description text NOT NULL,
    poster_url character varying(1000) NOT NULL,
    banner_url character varying(1000) NOT NULL,
    video_url character varying(1000) NOT NULL,
    rating numeric(3,1) NOT NULL,
    release_year integer NOT NULL,
    language character varying(100) NOT NULL,
    duration character varying(50) NOT NULL,
    is_trending boolean NOT NULL,
    is_popular boolean NOT NULL,
    is_latest boolean NOT NULL,
    is_top_rated boolean NOT NULL,
    "cast" text NOT NULL,
    crew text NOT NULL,
    content_type character varying(20) NOT NULL,
    display_order integer NOT NULL
);


--
-- Name: cine_verse_movie_genres; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cine_verse_movie_genres (
    id bigint NOT NULL,
    movie_id bigint NOT NULL,
    genre_id bigint NOT NULL
);


--
-- Name: cine_verse_movie_genres_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.cine_verse_movie_genres ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.cine_verse_movie_genres_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: cine_verse_movie_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.cine_verse_movie ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.cine_verse_movie_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: cine_verse_userprofile; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cine_verse_userprofile (
    id bigint NOT NULL,
    subscription_plan character varying(50) NOT NULL,
    avatar_url character varying(1000),
    user_id integer NOT NULL,
    favorites_order text NOT NULL,
    watchlist_order text NOT NULL
);


--
-- Name: cine_verse_userprofile_favorite_genres; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cine_verse_userprofile_favorite_genres (
    id bigint NOT NULL,
    userprofile_id bigint NOT NULL,
    genre_id bigint NOT NULL
);


--
-- Name: cine_verse_userprofile_favorite_genres_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.cine_verse_userprofile_favorite_genres ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.cine_verse_userprofile_favorite_genres_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: cine_verse_userprofile_favorites; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cine_verse_userprofile_favorites (
    id bigint NOT NULL,
    userprofile_id bigint NOT NULL,
    movie_id bigint NOT NULL
);


--
-- Name: cine_verse_userprofile_favorites_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.cine_verse_userprofile_favorites ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.cine_verse_userprofile_favorites_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: cine_verse_userprofile_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.cine_verse_userprofile ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.cine_verse_userprofile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: cine_verse_userprofile_watchlist; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cine_verse_userprofile_watchlist (
    id bigint NOT NULL,
    userprofile_id bigint NOT NULL,
    movie_id bigint NOT NULL
);


--
-- Name: cine_verse_userprofile_watchlist_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.cine_verse_userprofile_watchlist ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.cine_verse_userprofile_watchlist_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: cine_verse_watchhistory; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cine_verse_watchhistory (
    id bigint NOT NULL,
    watched_at timestamp with time zone NOT NULL,
    progress integer NOT NULL,
    movie_id bigint NOT NULL,
    user_id integer NOT NULL
);


--
-- Name: cine_verse_watchhistory_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.cine_verse_watchhistory ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.cine_verse_watchhistory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add user	4	add_user
14	Can change user	4	change_user
15	Can delete user	4	delete_user
16	Can view user	4	view_user
17	Can add content type	5	add_contenttype
18	Can change content type	5	change_contenttype
19	Can delete content type	5	delete_contenttype
20	Can view content type	5	view_contenttype
21	Can add session	6	add_session
22	Can change session	6	change_session
23	Can delete session	6	delete_session
24	Can view session	6	view_session
25	Can add genre	7	add_genre
26	Can change genre	7	change_genre
27	Can delete genre	7	delete_genre
28	Can view genre	7	view_genre
29	Can add movie	8	add_movie
30	Can change movie	8	change_movie
31	Can delete movie	8	delete_movie
32	Can view movie	8	view_movie
33	Can add user profile	9	add_userprofile
34	Can change user profile	9	change_userprofile
35	Can delete user profile	9	delete_userprofile
36	Can view user profile	9	view_userprofile
37	Can add watch history	10	add_watchhistory
38	Can change watch history	10	change_watchhistory
39	Can delete watch history	10	delete_watchhistory
40	Can view watch history	10	view_watchhistory
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
2	pbkdf2_sha256$720000$IyoYjZe3IJXA3JdN9TDE1h$zs8yoiLlzGo9dQz+5C7C7o1C3Jdt/DD+zQVkt0eBMdc=	\N	f	marcus	Marcus	Vance	marcus@cineverse.com	f	t	2026-06-09 12:18:33.927657+05:30
1	pbkdf2_sha256$720000$hnsOBQJQlTMyzO4RTMWUtA$9Mwv2dLdPSOH6zz5bUFObUBy/iV5zOao3+v9ooU7HDo=	2026-06-09 13:07:44.198013+05:30	t	admin			admin@cineverse.com	t	t	2026-06-09 12:18:32.816528+05:30
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: cine_verse_genre; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.cine_verse_genre (id, name, slug) FROM stdin;
1	Action	action
2	Sci-Fi	sci-fi
3	Drama	drama
4	Thriller	thriller
5	Comedy	comedy
6	Horror	horror
7	Adventure	adventure
\.


--
-- Data for Name: cine_verse_movie; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.cine_verse_movie (id, title, description, poster_url, banner_url, video_url, rating, release_year, language, duration, is_trending, is_popular, is_latest, is_top_rated, "cast", crew, content_type, display_order) FROM stdin;
51	Chernobyl	A dramatization of the true story of one of the worst man-made catastrophes in history: the catastrophic nuclear accident at Chernobyl.	https://image.tmdb.org/t/p/original/f67LHfAABmKz88mQJsyAzD522DZ.jpg	https://image.tmdb.org/t/p/original/3URK0z9PzpVNJrGE7XOuyy6KFzk.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.4	2019	English	TV Series	f	t	f	t	Jared Harris, Stellan Skarsgård, Emily Watson	Creator: Craig Mazin	series	510
3	The Dark Knight	When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.	https://alternativemovieposters.com/wp-content/uploads/2023/09/John-Hanley_DarkKnight.jpg	https://image.tmdb.org/t/p/original/cfT29Im5VDvjE0RpyKOSdCKZal7.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.7	2008	English	2h 32m	t	t	f	t	Christian Bale, Heath Ledger, Aaron Eckhart, Maggie Gyllenhaal	Director: Christopher Nolan	movie	60
52	The Boroughs	A gritty anthology exploring crime, community, and resilience across different neighborhoods of a modern metropolis.	https://www.artofvfx.com/wp-content/uploads/2026/04/boroughs_xlg.jpg	https://image.tmdb.org/t/p/original/iftYIh1OjJb99EOTHIrDcx59zWb.jpg	https://www.w3schools.com/html/mov_bbb.mp4	8.2	2022	English	TV Series	t	f	f	f	Ensemble Cast	Creators: Various	series	520
4	Inception	A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.	https://wallpapercat.com/w/full/9/6/1/304867-1536x2732-iphone-hd-inception-background-image.jpg	https://image.tmdb.org/t/p/original/8ZTVqvKDQ8emSGUEMjsS4yHAwrp.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.4	2010	English	2h 28m	f	t	f	t	Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page, Tom Hardy	Director: Christopher Nolan	movie	120
6	Gladiator	A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.	https://cdn.posteritati.com/posters/000/000/062/005/gladiator-md-web.jpg	https://image.tmdb.org/t/p/original/jhk6D8pim3yaByu1801kMoxXFaX.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.1	2000	English	2h 35m	f	t	f	t	Russell Crowe, Joaquin Phoenix, Connie Nielsen, Oliver Reed	Director: Ridley Scott	movie	150
53	Spider-Noir	A stylistic, noir-influenced animated series following a masked vigilante who navigates a shadowy multiverse of crime and paradox.	https://resizing.flixster.com/cctrdlqeQz3fN_jnPDpygBev4Dg=/fit-in/705x460/v2/https://resizing.flixster.com/-XZAfHZM39UwaGJIFWKAE8fS0ak=/v3/t/assets/p31566164_b_v12_aa.jpg	https://image.tmdb.org/t/p/original/6t2FvBr9DS8MOq0m5FAwPBCdAW5.jpg	https://www.w3schools.com/html/mov_bbb.mp4	8.6	2024	English	TV Series	f	f	t	f	Voice Cast	Creators: Creative Studio	series	530
49	Moon Knight	A complex antihero with dissociative identity disorder becomes entangled in a deadly mystery involving Egyptian gods.	https://m.media-amazon.com/images/M/MV5BNDAzNmYwZjgtNDc3YS00ZDMyLTk0MjktMTg4MGNmNGU3MjlhXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg	https://image.tmdb.org/t/p/original/iux1vKPT7Vw1AzetZb4Jz6wfYsm.jpg	https://www.w3schools.com/html/mov_bbb.mp4	7.7	2022	English	TV Series	t	f	t	f	Oscar Isaac, Ethan Hawke, May Calamawy	Creator: Jeremy Slater	series	490
50	Dark	A time-travel mystery that follows four interconnected families as they uncover a sinister time loop spanning several generations.	https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS2eWtMqKEfm3T-HJAq7DwgVk1bgvKvtPkjKQ&s	https://image.tmdb.org/t/p/original/3jDXL4Xvj3AzDOF6UH1xeyHW8MH.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.0	2017	German	TV Series	f	t	f	t	Louis Hofmann, Karoline Eichhorn, Lisa Vicari	Creators: Baran bo Odar, Jantje Friese	series	500
1	Interstellar	The adventures of a group of explorers who make use of a newly discovered wormhole to surpass the limitations on human space travel and conquer the vast distances involved in an interstellar voyage.	https://i.pinimg.com/originals/8e/0d/ab/8e0dab8699be85720ce55845065bf6dc.jpg	https://wallpaperaccess.com/full/300686.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.8	2014	English	2h 49m	t	t	f	t	Matthew McConaughey, Anne Hathaway, Jessica Chastain, Michael Caine	Director: Christopher Nolan	movie	10
13	The Conjuring	Paranormal investigators Ed and Lorraine Warren work to help a family terrorized by a dark presence in their farmhouse.	https://images.static-bluray.com/movies/uvcovers/3274_large.jpg	https://image.tmdb.org/t/p/original/ecKQlAEG95k62SMGhvX83oEqANK.jpg	https://www.w3schools.com/html/mov_bbb.mp4	8.5	2013	English	1h 52m	f	t	f	f	Vera Farmiga, Patrick Wilson, Lili Taylor, Ron Livingston	Director: James Wan	movie	110
19	Shutter Island	In 1954, a U.S. Marshal investigates the disappearance of a murderer who escaped from a hospital for the criminally insane.	https://w0.peakpx.com/wallpaper/98/690/HD-wallpaper-shutter-island-screen-printed-movie-poster.jpg	https://image.tmdb.org/t/p/original/rbZvGN1A1QyZuoKzhCw8QPmf2q0.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.0	2010	English	2h 18m	t	t	f	f	Leonardo DiCaprio, Mark Ruffalo, Ben Kingsley, Michelle Williams	Director: Martin Scorsese	movie	270
10	The Shawshank Redemption	Over the course of several years, two convicts form a friendship, seeking consolation and, eventually, redemption through basic compassion.	https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRD1VWS5ADAVUQZbSi0trMPSZfIwOLZ2VYPSw&s	https://image.tmdb.org/t/p/original/zfbjgQE1uSd9wiPTX4VzsLi0rGG.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.9	1994	English	2h 22m	t	f	f	t	Tim Robbins, Morgan Freeman, Bob Gunton, William Sadler	Director: Frank Darabont	movie	170
14	Hereditary	A grieving family is haunted by tragic and disturbing occurrences after the death of their secretive grandmother.	https://m.media-amazon.com/images/M/MV5BYTcxNzU0MzctOTJjZS00NzYwLWFkZDMtNzliY2VjMzBiNWM1XkEyXkFqcGc@._V1_.jpg	https://image.tmdb.org/t/p/original/gJbTXKNTL6O7r7PzF6ZRkJGBlPp.jpg	https://www.w3schools.com/html/mov_bbb.mp4	8.4	2018	English	2h 07m	t	f	f	f	Toni Collette, Milly Shapiro, Alex Wolff, Gabriel Byrne	Director: Ari Aster	movie	90
21	Superbad	Two co-dependent high school seniors are forced to deal with separation anxiety after their plan to stage a booze-fueled party goes awry.	https://www.acmodasi.in/amdb/images/movie/z/k/superbad-2007-39916.jpg	https://image.tmdb.org/t/p/original/coru98UcFBzJIU7bxZguxaePgu0.jpg	https://www.w3schools.com/html/mov_bbb.mp4	8.3	2007	English	1h 53m	t	t	f	f	Jonah Hill, Michael Cera, Christopher Mintz-Plasse, Bill Hader	Director: Greg Mottola	movie	220
20	The Hangover	Three buddies wake up from a bachelor party in Las Vegas with no memory of the previous night and the bachelor missing.	https://image.tmdb.org/t/p/original/wzLMIElewg7XFATaaODnncoe6Td.jpg	https://image.tmdb.org/t/p/original/iuRVt8tFiXDPGgzavhuSa3QHRxD.jpg	https://www.w3schools.com/html/mov_bbb.mp4	8.2	2009	English	1h 40m	f	t	f	f	Bradley Cooper, Ed Helms, Zach Galifianakis, Justin Bartha	Director: Todd Phillips	movie	210
9	The Godfather	The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.	https://wallpapercave.com/wp/wp12115434.jpg	https://image.tmdb.org/t/p/original/tSPT36ZKlP2WVHJLM4cQPLSzv3b.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.9	1972	English	2h 55m	f	t	f	t	Marlon Brando, Al Pacino, James Caan, Diane Keaton	Director: Francis Ford Coppola	movie	130
18	Spider-Man: No Way Home	Peter Parker's life and reputation are upended when a spell gone wrong opens the multiverse and brings dangerous visitors into his world.	https://static.wikia.nocookie.net/marvelcinematicuniverse/images/1/1d/Spider-Man_No_Way_Home_JP_Poster.jpg/revision/latest/thumbnail/width/360/height/360?cb=20211125071618	https://image.tmdb.org/t/p/original/tyQo080tijexyUHBvWPwQt26bZa.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.1	2021	English	2h 28m	t	t	t	f	Tom Holland, Zendaya, Benedict Cumberbatch, Jacob Batalon	Director: Jon Watts	movie	70
22	It	In the summer of 1989, a group of bullied kids band together to destroy a shape-shifting monster, which disguises itself as a clown and preys on the children of their town.	https://i.ebayimg.com/00/s/MTYwMFgxMDg2/z/qHwAAOSw1Y5dcuMC/$_57.JPG?set_id=8800005007	https://image.tmdb.org/t/p/original/qVGpxnjrGlHaSTCqTQI6viBDSfp.jpg	https://www.w3schools.com/html/mov_bbb.mp4	8.4	2017	English	2h 15m	f	t	f	f	Bill Skarsgård, Jaeden Martell, Finn Wolfhard, Sophia Lillis	Director: Andy Muschietti	movie	230
33	Stranger Things	Currently trending on Netflix. When a young boy vanishes, a small town uncovers a mystery involving secret experiments, terrifying supernatural forces and one strange little girl.	https://static.posters.cz/image/1300/297827.jpg	https://image.tmdb.org/t/p/original/56v2KjBlU4XaOv9rVYEQypROD7P.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.6	2025	English	TV Series	t	t	t	t	Millie Bobby Brown, Finn Wolfhard, Winona Ryder, David Harbour	Creators: The Duffer Brothers	series	330
31	M3GAN	A toy-company roboticist builds a life-like doll that begins to take on a life of its own, leading to terrifying consequences.	https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSgL6_djuzpvG6Hl4LDMfSOCRNgPsbqONAQ_Q&s	https://image.tmdb.org/t/p/original/qd4EKTuudkws9lW76Dn9C0tnuVA.jpg	https://www.w3schools.com/html/mov_bbb.mp4	8.0	2022	English	1h 42m	f	t	f	f	Allison Williams, Violet McGraw, Ronny Chieng	Director: Gerard Johnstone	movie	320
27	The Lord of the Rings: The Fellowship of the Ring	A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.	https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQEaOTjjsH93_nbzlb8EI124CNG6wq4UUTfhA&s	https://image.tmdb.org/t/p/original/oiwc338EoBgS4sEI2ixAny4KQKg.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.8	2001	English	2h 58m	t	t	f	t	Elijah Wood, Ian McKellen, Orlando Bloom, Viggo Mortensen	Director: Peter Jackson	movie	260
34	The Boys	Currently trending on Prime Video. A fun, gritty, and dark superhero series focusing on a group of vigilantes set out to take down corrupt superheroes who abuse their superpowers.	https://image.tmdb.org/t/p/original/in1R2dDc421JxsoRWaIIAqVI2KE.jpg	https://image.tmdb.org/t/p/original/bq28ajZaoMyzEIm6REelqyqtEDZ.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.4	2024	English	TV Series	t	t	f	t	Karl Urban, Jack Quaid, Antony Starr, Erin Moriarty	Creator: Eric Kripke	series	340
35	Shōgun	Currently trending on Disney+ Hotstar. In Japan in the year 1600, Lord Yoshii Toranaga struggles for his life as his enemies on the Council of Regents unite against him.	https://image.tmdb.org/t/p/original/knnGreFnQqhufzg9AqjzeMD7k5I.jpg	https://image.tmdb.org/t/p/original/6Tb87q9Tog30F5AAHh1gyDT2Vve.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.5	2024	Japanese	TV Series	t	t	t	t	Hiroyuki Sanada, Cosmo Jarvis, Anna Sawai	Creators: Rachel Kondo, Justin Marks	series	350
36	Breaking Bad	A high school chemistry teacher diagnosed with inoperable lung cancer turns to manufacturing and selling methamphetamine with a former student in order to secure his family's future.	https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQeyQJOmXbTuKCFsSwBdtE6vCHJa1Up25JuQ&s	https://image.tmdb.org/t/p/original/tsRy63Mu5cu8etL1X7ZLyf7UP1M.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.9	2008	English	TV Series	f	t	f	t	Bryan Cranston, Aaron Paul, Anna Gunn, Bob Odenkirk	Creator: Vince Gilligan	series	360
38	The Office	A mockumentary on a group of typical office workers, where the workday consists of ego clashes, inappropriate behavior, and tedium.	https://wallpapercat.com/w/full/c/2/1/172504-1280x1922-samsung-hd-the-office-tv-series-background.jpg	https://image.tmdb.org/t/p/original/mLyW3UTgi2lsMdtueYODcfAB9Ku.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.2	2005	English	TV Series	f	t	f	t	Steve Carell, Rainn Wilson, John Krasinski, Jenna Fischer	Developer: Greg Daniels	series	380
39	Friends	Follows the personal and professional lives of six twenty to thirty-something-year-old friends living in Manhattan.	https://image.tmdb.org/t/p/original/2koX1xLkpTQM4IZebYvKysFW1Nh.jpg	https://image.tmdb.org/t/p/original/m3Jev59mJLyUp5bXhY5SVfIBZI0.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.0	1994	English	TV Series	f	t	f	t	Jennifer Aniston, Courteney Cox, Lisa Kudrow, Matt LeBlanc, Matthew Perry, David Schwimmer	Creators: David Crane, Marta Kauffman	series	390
43	Wednesday	Follows Wednesday Addams' years as a student at Nevermore Academy, as she attempts to master her emerging psychic ability, thwart a monstrous killing spree, and solve the mystery that embroiled her parents.	https://4kwallpapers.com/images/wallpapers/wednesday-netflix-2160x3840-23051.jpg	https://image.tmdb.org/t/p/original/iHSwvRVsRyxpX7FE7GbviaDvgGZ.jpg	https://www.w3schools.com/html/mov_bbb.mp4	8.8	2022	English	TV Series	f	t	f	f	Jenna Ortega, Gwendoline Christie, Riki Lindhome	Creators: Alfred Gough, Miles Millar	series	430
40	Ted Lasso	American college football coach Ted Lasso heads to London to manage a struggling English Premier League football team, AFC Richmond.	https://lh4.googleusercontent.com/proxy/0KyQhkSlogOqldlFAMeu9xrUyJ2kfb6jLRwAnnhrbIXQgidiWbSK1NuD7Egl7ZfKN6wrSEQXMr0rHjBAxT51uP92Lpc	https://image.tmdb.org/t/p/original/gEQkOMmnJcoh9Hh1vk7fpVYnksR.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.1	2020	English	TV Series	t	t	f	f	Jason Sudeikis, Hannah Waddingham, Jeremy Swift, Phil Dunster	Creators: Jason Sudeikis, Bill Lawrence	series	400
48	Alice in the Borderland	A group of friends must survive dangerous games in an abandoned Tokyo that has become a ruthless alternate world.	https://i.pinimg.com/736x/a3/bb/b1/a3bbb19fdffd2343159cacdb98c198e3.jpg	https://image.tmdb.org/t/p/original/Ac8ruycRXzgcsndTZFK6ouGA0FA.jpg	https://www.w3schools.com/html/mov_bbb.mp4	7.7	2020	Japanese	TV Series	f	t	f	t	Kento Yamazaki, Tao Tsuchiya, Nijiro Murakami	Creators: Haro Aso, Shinsuke Sato	series	480
42	The Night Manager	Currently trending on Disney+ Hotstar. A hotel night manager is recruited by a government agent to infiltrate the inner circle of a ruthless arms dealer.	https://image.tmdb.org/t/p/original/1MccRnw41qQjREuZkovqP2UX1i3.jpg	https://image.tmdb.org/t/p/original/2vAOdruqvx9GojXxKi3xVsZZvKU.jpg	https://www.w3schools.com/html/mov_bbb.mp4	8.7	2023	Hindi	TV Series	t	f	t	f	Anil Kapoor, Aditya Roy Kapur, Sobhita Dhulipala	Director: Sandeep Modi	series	420
41	The Legend of Vox Machina	They're rowdy, they're ragtag, they're misfits turned mercenaries for hire. Vox Machina is more interested in easy money and cheap ale than actually protecting the realm.	https://lh5.googleusercontent.com/proxy/li3CV1KsErBqobbmnYN30DrbJn8dt46mscPbyvKIHP4EF_kkxt1j7g3lodXBDRk99loPPpruvW9wpsNna6CCyBTYAL-lxZ44RUuYXZJqj2k	https://image.tmdb.org/t/p/original/qCGwPCwlSiLdlYinzy9rSQDjQX1.jpg	https://www.w3schools.com/html/mov_bbb.mp4	8.9	2022	English	TV Series	t	f	t	f	Laura Bailey, Ashley Johnson, Matthew Mercer, Liam O'Brien	Creators: Critical Role	series	410
44	The Last of Us	After a global pandemic destroys civilization, a hardened survivor takes charge of a 14-year-old girl who may be humanity's last hope.	https://image.tmdb.org/t/p/original/dmo6TYuuJgaYinXBPjrgG9mB5od.jpg	https://image.tmdb.org/t/p/original/acevLdSl5I2MK5RYAm7gwAndt1w.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.4	2023	English	TV Series	f	t	f	t	Pedro Pascal, Bella Ramsey, Gabriel Luna	Creators: Craig Mazin, Neil Druckmann	series	440
45	Squid Game	Hundreds of cash-strapped players accept a strange invitation to compete in children's games. Inside, a tempting prize awaits with deadly high stakes.	https://image.tmdb.org/t/p/original/1QdXdRYfktUSONkl1oD5gc6Be0s.jpg	https://image.tmdb.org/t/p/original/2meX1nMdScFOoV4370rqHWKmXhY.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.1	2021	Korean	TV Series	t	t	f	f	Lee Jung-jae, Park Hae-soo, Wi Ha-jun	Creator: Hwang Dong-hyuk	series	450
46	The Haunting of Hill House	Flashing between past and present, a fractured family confronts haunting memories of their old home and the terrifying events that drove them from it.	https://image.tmdb.org/t/p/original/38PkhBGRQtmVx2drvPik3F42qHO.jpg	https://image.tmdb.org/t/p/original/sNtNXwtEbdw4LaCFxFQwL2Jv4yW.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.2	2018	English	TV Series	f	t	f	t	Michiel Huisman, Carla Gugino, Timothy Hutton, Elizabeth Reaser	Creator: Mike Flanagan	series	460
47	From	Unraveling the mystery of a nightmarish town that traps everyone who enters, the residents fight to survive while searching for a way out.	https://image.tmdb.org/t/p/original/uV65yaFkw6B4KHXAsBYui0KvJq.jpg	https://image.tmdb.org/t/p/original/xLdw1xdHocKYFFvx7w41NchXMfJ.jpg	https://www.w3schools.com/html/mov_bbb.mp4	7.8	2022	English	TV Series	t	t	f	f	Harold Perrineau, Catalina Sandino Moreno, Eion Bailey	Creator: John Griffin	series	470
37	Succession	The Roy family is known for controlling the biggest media and entertainment company in the world. However, their world changes when their father steps down from the company.	https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSa7WAx4xvdNwCJtuFpa78U8lptX94jPuM41A&s	https://image.tmdb.org/t/p/original/bcdUYUFk8GdpZJPiSAas9UeocLH.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.4	2018	English	TV Series	t	t	f	t	Brian Cox, Jeremy Strong, Sarah Snook, Kieran Culkin	Creator: Jesse Armstrong	series	370
5	Oppenheimer	The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb.	https://tse3.mm.bing.net/th/id/OIP.x3NOySbSqWJoXh40qldQkgAAAA?w=440&h=660&rs=1&pid=ImgDetMain&o=7&rm=3	https://image.tmdb.org/t/p/original/neeNHeXjMF5fXoCJRsOmkNGC7q.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.3	2023	English	3h 00m	t	t	t	f	Cillian Murphy, Emily Blunt, Matt Damon, Robert Downey Jr.	Director: Christopher Nolan	movie	20
30	Talk to Me	When a group of friends discover how to conjure spirits using an embalmed hand, they become hooked on the new thrill, until one of them goes too far and unleashes terrifying supernatural forces.	https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTWlBOR2EuEO3Cod7-rQumorBDOKX91wf1_VQ&s	https://image.tmdb.org/t/p/original/46Os8U0DEPmI0OnvKDxucl6SLVZ.jpg	https://www.w3schools.com/html/mov_bbb.mp4	8.3	2023	English	1h 35m	t	f	t	f	Sophie Wilde, Alexandra Jensen, Joe Bird	Directors: Danny Philippou, Michael Philippou	movie	310
32	Project Hail Mary	A lone astronaut embarks on a desperate, last-chance mission to save humanity, discovering unexpected allies and relying on ingenuity to survive.	https://media.themoviedb.org/t/p/w220_and_h330_face/mSevmySMoq6E5JZVrLXACUUo0n5.jpg	https://image.tmdb.org/t/p/original/yihdXomYb5kTeSivtFndMy5iDmf.jpg	https://www.w3schools.com/html/mov_bbb.mp4	8.5	2024	English	2h 30m	f	t	t	f	Ryan Gosling, Emily Blunt	Director: Phil Lord, Christopher Miller	movie	100
25	Spider-Man: Across the Spider-Verse	Miles Morales catapults across the Multiverse, where he encounters a team of Spider-People charged with protecting its very existence. When the heroes clash on how to handle a new threat, Miles must redefine what it means to be a hero.	https://preview.redd.it/official-poster-for-spider-man-across-the-spider-verse-v0-yogt3cuj727a1.jpg?width=640&crop=smart&auto=webp&s=b5d25d425beaae300ed10c7237e015816e0fe01b	https://image.tmdb.org/t/p/original/9xfDWXAUbFXQK585JvByT5pEAhe.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.5	2023	English	2h 20m	t	t	t	f	Shameik Moore, Hailee Steinfeld, Oscar Isaac, Jake Johnson	Directors: Joaquim Dos Santos, Kemp Powers	movie	250
23	The Matrix	When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth--the life he knows is the elaborate deception of an evil cyber-intelligence.	https://c4.wallpaperflare.com/wallpaper/614/687/784/movies-matrix-movie-poster-poster-the-matrix-resurrections-hd-wallpaper-preview.jpg	https://image.tmdb.org/t/p/original/tlm8UkiQsitc8rSuIAscQDCnP8d.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.5	1999	English	2h 16m	f	t	f	t	Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving	Director: The Wachowskis	movie	240
16	Avatar: The Way of Water	Jake Sully lives with his newfound family formed on the extrasolar moon Pandora. Once a familiar threat returns to finish what was previously started, Jake must work with Neytiri and the army of the Na'vi race to protect their home.	https://lh3.googleusercontent.com/proxy/bhvo3KRlQs3DIkuenM5mhHive1ZrURmR4TaVRGNTvgdU4jujs0y_1t29-PrHUJ-8uNo6x7NDCLk5CziFrG9nIItjVRNC4Qm4OSQ_AXNl3F1Ph_BbjeyrobvL	https://image.tmdb.org/t/p/original/qnzQm0PCVnSyv1dqpVmRgMWHbLD.jpg	https://www.w3schools.com/html/mov_bbb.mp4	8.7	2022	English	3h 12m	t	t	f	f	Sam Worthington, Zoe Saldana, Sigourney Weaver, Kate Winslet	Director: James Cameron	movie	30
26	Avengers: Endgame	After the devastating events of Avengers: Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos' actions and restore balance to the universe.	https://i.pinimg.com/736x/21/67/17/21671739d7ab8cda661c47af6880f86a.jpg	https://image.tmdb.org/t/p/original/ulzhLuWrPK07P1YkdWQLZnQh1JL.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.2	2019	English	3h 01m	f	t	f	t	Robert Downey Jr., Chris Evans, Mark Ruffalo, Chris Hemsworth	Directors: Anthony Russo, Joe Russo	movie	40
7	Mad Max: Fury Road	In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search for her homeland with the aid of a group of female prisoners, a psychotic worshiper, and a drifter named Max.	https://images.justwatch.com/poster/8716732/s718/mad-max-fury-road.jpg	https://image.tmdb.org/t/p/original/uT895WNwm0aIJRtGizcQhrejWUo.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.0	2015	English	2h 00m	t	t	f	f	Tom Hardy, Charlize Theron, Nicholas Hoult, Zoë Kravitz	Director: George Miller	movie	160
28	The Shining	A family heads to an isolated hotel for the winter where a sinister presence influences the father into violence, while his psychic son sees horrific forebodings from both past and future.	https://preview.redd.it/poster-for-the-re-release-of-stanley-kubricks-the-shining-v0-j4awcuw61fo31.jpg?auto=webp&s=61908186e652c6f2281429c688bca2b4b11f8840	https://image.tmdb.org/t/p/original/mmd1HnuvAzFc4iuVJcnBrhDNEKr.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.0	1980	English	2h 26m	f	t	f	t	Jack Nicholson, Shelley Duvall, Danny Lloyd, Scatman Crothers	Director: Stanley Kubrick	movie	280
17	Blade Runner 2049	A new blade runner, LAPD Officer K, unearths a long-buried secret that has the potential to plunge what's left of society into chaos.	https://m.media-amazon.com/images/M/MV5BNzA1Njg4NzYxOV5BMl5BanBnXkFtZTgwODk5NjU3MzI@._V1_FMjpg_UX1000_.jpg	https://image.tmdb.org/t/p/original/mVr0UiqyltcfqxbAUcLl9zWL8ah.jpg	https://www.w3schools.com/html/mov_bbb.mp4	8.9	2017	English	2h 44m	t	t	f	f	Ryan Gosling, Harrison Ford, Ana de Armas, Sylvia Hoeks	Director: Denis Villeneuve	movie	200
15	A Quiet Place	A family must navigate their lives in silence to avoid mysterious creatures that hunt by sound.	https://lh5.googleusercontent.com/proxy/NUylUXnFwN2gzEqgzJpQAuM7DQGp0BH6f-HDFNao8O-2g0KrZjBJ6D-KiOG7L-j3ftkawdxHZZfdkQu9XeFEHnd0LnnPJnIHVOqE-Z8XSVDgHw	https://image.tmdb.org/t/p/original/nHRUtBwFNnNN70vcQ7lAsjc2T6S.jpg	https://www.w3schools.com/html/mov_bbb.mp4	8.8	2018	English	1h 30m	f	t	f	t	Emily Blunt, John Krasinski, Millicent Simmonds, Noah Jupe	Director: John Krasinski	movie	190
11	Parasite	Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.	https://image.tmdb.org/t/p/original/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg	https://image.tmdb.org/t/p/original/TU9NIjwzjoKPwQHoHshkFcQUCG.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.3	2019	Korean	2h 12m	f	t	f	t	Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong, Choi Woo-shik	Director: Bong Joon Ho	movie	140
24	Spirited Away	During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, and where humans are changed into beasts.	https://wallpapercat.com/w/full/8/f/a/34495-1536x2732-samsung-hd-spirited-away-background-photo.jpg	https://image.tmdb.org/t/p/original/dyJvKsNs2KP8qQnAXbRwDjblViy.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.6	2001	Japanese	2h 05m	t	f	f	t	Rumi Hiiragi, Miyu Irino, Mari Natsuki	Director: Hayao Miyazaki	movie	290
29	A Nightmare on Elm Street	The monstrous spirit of a slain child murderer seeks revenge by invading the dreams of teenagers whose parents were responsible for his untimely demise.	https://images.moviesanywhere.com/1d30e66f0447b8a5f164441112fbc091/e64b6e92-c2f5-47d1-8175-4b0dd47eb66b.jpg	https://image.tmdb.org/t/p/original/nzSjTiecdosBfwMGAdpt9CxltCI.jpg	https://www.w3schools.com/html/mov_bbb.mp4	8.1	1984	English	1h 31m	t	f	f	f	Heather Langenkamp, Johnny Depp, Robert Englund	Director: Wes Craven	movie	300
2	Dune: Part Two	Follow the mythic journey of Paul Atreides as he unites with Chani and the Fremen while on a path of revenge against the conspirators who destroyed his family.	https://m.media-amazon.com/images/M/MV5BNTc0YmQxMjEtODI5MC00NjFiLTlkMWUtOGQ5NjFmYWUyZGJhXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg	https://image.tmdb.org/t/p/original/xOMo8BRK7PfcJv9JCnx7s5hj0PX.jpg	https://www.w3schools.com/html/mov_bbb.mp4	9.6	2024	English	2h 46m	t	t	t	f	Timothée Chalamet, Zendaya, Rebecca Ferguson, Javier Bardem	Director: Denis Villeneuve	movie	50
12	Get Out	A young African-American visits his white girlfriend's parents for the weekend, where his simmering uneasiness about their reception eventually reaches a boiling point.	https://m.media-amazon.com/images/M/MV5BOGMzMjFiMDUtZWQ5Ny00MTUyLWEyYzItMzcwNzJjNzBmMjI4XkEyXkFqcGc@._V1_.jpg	https://image.tmdb.org/t/p/original/o8dPH0ZSIyyViP6rjRX1djwCUwI.jpg	https://www.w3schools.com/html/mov_bbb.mp4	8.7	2017	English	1h 44m	t	t	f	f	Daniel Kaluuya, Allison Williams, Bradley Whitford, Catherine Keener	Director: Jordan Peele	movie	180
8	John Wick: Chapter 4	John Wick uncovers a path to defeating The High Table. But before he can earn his freedom, Wick must face off against a new enemy with powerful alliances across the globe.	https://media.themoviedb.org/t/p/w220_and_h330_face/vZloFAK7NmvMGKE7VkF5UHaz0I.jpg	https://image.tmdb.org/t/p/original/vZloFAK7NmvMGKE7VkF5UHaz0I.jpg	https://www.w3schools.com/html/mov_bbb.mp4	8.9	2023	English	2h 49m	t	f	t	f	Keanu Reeves, Donnie Yen, Bill Skarsgård, Laurence Fishburne	Director: Chad Stahelski	movie	80
\.


--
-- Data for Name: cine_verse_movie_genres; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.cine_verse_movie_genres (id, movie_id, genre_id) FROM stdin;
203	38	5
204	39	5
205	43	4
4	2	2
5	2	7
6	2	1
206	43	5
207	43	6
208	41	1
10	4	1
11	4	2
12	4	4
209	41	5
210	41	7
211	48	1
212	48	2
213	48	4
214	50	2
215	50	3
216	50	4
23	9	3
24	9	4
25	10	3
29	12	6
30	12	4
31	13	6
32	13	4
223	51	3
35	15	6
36	15	2
37	15	4
224	51	4
225	52	3
226	53	1
41	17	2
42	17	4
43	17	3
44	18	1
45	18	7
46	18	2
227	53	5
228	53	7
49	20	5
50	21	5
51	22	6
52	22	4
53	23	2
54	23	1
57	25	1
58	25	7
59	25	2
63	27	7
64	27	1
65	27	3
70	30	6
71	30	4
72	31	6
73	31	2
74	32	2
75	32	3
76	32	7
80	34	1
81	34	2
82	34	5
83	35	3
84	35	1
85	36	3
86	36	4
91	40	5
92	40	3
96	42	4
97	42	3
98	42	1
102	44	3
103	44	1
104	44	2
105	45	4
106	45	3
107	45	1
108	46	6
109	46	3
110	47	6
111	47	4
115	49	1
116	49	7
117	49	3
136	1	2
137	1	3
138	1	7
139	3	1
140	3	3
141	3	4
144	5	3
145	5	4
146	6	1
147	6	3
148	6	7
149	7	1
150	7	2
151	7	7
158	8	1
159	8	4
160	11	3
161	11	4
162	11	5
169	16	1
170	16	2
171	16	7
172	14	3
173	14	6
174	19	3
175	19	4
176	26	1
177	26	2
178	26	7
179	28	3
180	28	6
181	29	4
182	29	6
187	24	3
188	24	7
189	37	3
190	37	5
200	33	2
201	33	4
202	33	6
\.


--
-- Data for Name: cine_verse_userprofile; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.cine_verse_userprofile (id, subscription_plan, avatar_url, user_id, favorites_order, watchlist_order) FROM stdin;
2	Premium	\N	2		
1	Premium	\N	1		
\.


--
-- Data for Name: cine_verse_userprofile_favorite_genres; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.cine_verse_userprofile_favorite_genres (id, userprofile_id, genre_id) FROM stdin;
1	2	1
2	2	2
\.


--
-- Data for Name: cine_verse_userprofile_favorites; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.cine_verse_userprofile_favorites (id, userprofile_id, movie_id) FROM stdin;
1	2	3
2	2	4
3	2	5
\.


--
-- Data for Name: cine_verse_userprofile_watchlist; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.cine_verse_userprofile_watchlist (id, userprofile_id, movie_id) FROM stdin;
1	2	1
2	2	2
3	2	3
\.


--
-- Data for Name: cine_verse_watchhistory; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.cine_verse_watchhistory (id, watched_at, progress, movie_id, user_id) FROM stdin;
1	2026-06-09 12:18:34.961688+05:30	75	6	2
2	2026-06-09 12:18:34.96617+05:30	50	7	2
3	2026-06-09 12:18:34.968187+05:30	40	8	2
4	2026-06-09 12:18:34.969189+05:30	95	9	2
5	2026-06-09 12:18:34.976721+05:30	100	1	1
6	2026-06-09 12:18:34.97974+05:30	20	2	1
7	2026-06-09 21:20:48.934893+05:30	0	32	1
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	cine_verse	genre
8	cine_verse	movie
9	cine_verse	userprofile
10	cine_verse	watchhistory
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2026-06-09 12:17:48.593999+05:30
2	auth	0001_initial	2026-06-09 12:17:48.76848+05:30
3	admin	0001_initial	2026-06-09 12:17:48.81637+05:30
4	admin	0002_logentry_remove_auto_add	2026-06-09 12:17:48.835204+05:30
5	admin	0003_logentry_add_action_flag_choices	2026-06-09 12:17:48.880702+05:30
6	contenttypes	0002_remove_content_type_name	2026-06-09 12:17:48.918329+05:30
7	auth	0002_alter_permission_name_max_length	2026-06-09 12:17:48.935591+05:30
8	auth	0003_alter_user_email_max_length	2026-06-09 12:17:48.952705+05:30
9	auth	0004_alter_user_username_opts	2026-06-09 12:17:48.967259+05:30
10	auth	0005_alter_user_last_login_null	2026-06-09 12:17:48.980262+05:30
11	auth	0006_require_contenttypes_0002	2026-06-09 12:17:48.983257+05:30
12	auth	0007_alter_validators_add_error_messages	2026-06-09 12:17:48.99626+05:30
13	auth	0008_alter_user_username_max_length	2026-06-09 12:17:49.019822+05:30
14	auth	0009_alter_user_last_name_max_length	2026-06-09 12:17:49.034036+05:30
15	auth	0010_alter_group_name_max_length	2026-06-09 12:17:49.05105+05:30
16	auth	0011_update_proxy_permissions	2026-06-09 12:17:49.062589+05:30
17	auth	0012_alter_user_first_name_max_length	2026-06-09 12:17:49.076329+05:30
18	cine_verse	0001_initial	2026-06-09 12:17:49.258247+05:30
19	cine_verse	0002_remove_userprofile_favorite_genre_and_more	2026-06-09 12:17:49.337078+05:30
20	cine_verse	0003_movie_content_type	2026-06-09 12:17:49.353526+05:30
21	cine_verse	0004_movie_display_order	2026-06-09 12:17:49.370691+05:30
22	cine_verse	0005_userprofile_favorites_order_and_more	2026-06-09 12:17:49.422842+05:30
23	sessions	0001_initial	2026-06-09 12:17:49.442021+05:30
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 40, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 2, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: cine_verse_genre_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.cine_verse_genre_id_seq', 7, true);


--
-- Name: cine_verse_movie_genres_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.cine_verse_movie_genres_id_seq', 228, true);


--
-- Name: cine_verse_movie_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.cine_verse_movie_id_seq', 53, true);


--
-- Name: cine_verse_userprofile_favorite_genres_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.cine_verse_userprofile_favorite_genres_id_seq', 2, true);


--
-- Name: cine_verse_userprofile_favorites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.cine_verse_userprofile_favorites_id_seq', 3, true);


--
-- Name: cine_verse_userprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.cine_verse_userprofile_id_seq', 2, true);


--
-- Name: cine_verse_userprofile_watchlist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.cine_verse_userprofile_watchlist_id_seq', 3, true);


--
-- Name: cine_verse_watchhistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.cine_verse_watchhistory_id_seq', 7, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 10, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 23, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: cine_verse_genre cine_verse_genre_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cine_verse_genre
    ADD CONSTRAINT cine_verse_genre_pkey PRIMARY KEY (id);


--
-- Name: cine_verse_genre cine_verse_genre_slug_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cine_verse_genre
    ADD CONSTRAINT cine_verse_genre_slug_key UNIQUE (slug);


--
-- Name: cine_verse_movie_genres cine_verse_movie_genres_movie_id_genre_id_949ee331_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cine_verse_movie_genres
    ADD CONSTRAINT cine_verse_movie_genres_movie_id_genre_id_949ee331_uniq UNIQUE (movie_id, genre_id);


--
-- Name: cine_verse_movie_genres cine_verse_movie_genres_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cine_verse_movie_genres
    ADD CONSTRAINT cine_verse_movie_genres_pkey PRIMARY KEY (id);


--
-- Name: cine_verse_movie cine_verse_movie_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cine_verse_movie
    ADD CONSTRAINT cine_verse_movie_pkey PRIMARY KEY (id);


--
-- Name: cine_verse_userprofile_favorite_genres cine_verse_userprofile_f_userprofile_id_genre_id_5bdbe273_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cine_verse_userprofile_favorite_genres
    ADD CONSTRAINT cine_verse_userprofile_f_userprofile_id_genre_id_5bdbe273_uniq UNIQUE (userprofile_id, genre_id);


--
-- Name: cine_verse_userprofile_favorites cine_verse_userprofile_f_userprofile_id_movie_id_ef889f9b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cine_verse_userprofile_favorites
    ADD CONSTRAINT cine_verse_userprofile_f_userprofile_id_movie_id_ef889f9b_uniq UNIQUE (userprofile_id, movie_id);


--
-- Name: cine_verse_userprofile_favorite_genres cine_verse_userprofile_favorite_genres_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cine_verse_userprofile_favorite_genres
    ADD CONSTRAINT cine_verse_userprofile_favorite_genres_pkey PRIMARY KEY (id);


--
-- Name: cine_verse_userprofile_favorites cine_verse_userprofile_favorites_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cine_verse_userprofile_favorites
    ADD CONSTRAINT cine_verse_userprofile_favorites_pkey PRIMARY KEY (id);


--
-- Name: cine_verse_userprofile cine_verse_userprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cine_verse_userprofile
    ADD CONSTRAINT cine_verse_userprofile_pkey PRIMARY KEY (id);


--
-- Name: cine_verse_userprofile cine_verse_userprofile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cine_verse_userprofile
    ADD CONSTRAINT cine_verse_userprofile_user_id_key UNIQUE (user_id);


--
-- Name: cine_verse_userprofile_watchlist cine_verse_userprofile_w_userprofile_id_movie_id_fba4c27a_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cine_verse_userprofile_watchlist
    ADD CONSTRAINT cine_verse_userprofile_w_userprofile_id_movie_id_fba4c27a_uniq UNIQUE (userprofile_id, movie_id);


--
-- Name: cine_verse_userprofile_watchlist cine_verse_userprofile_watchlist_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cine_verse_userprofile_watchlist
    ADD CONSTRAINT cine_verse_userprofile_watchlist_pkey PRIMARY KEY (id);


--
-- Name: cine_verse_watchhistory cine_verse_watchhistory_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cine_verse_watchhistory
    ADD CONSTRAINT cine_verse_watchhistory_pkey PRIMARY KEY (id);


--
-- Name: cine_verse_watchhistory cine_verse_watchhistory_user_id_movie_id_e7bc2c96_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cine_verse_watchhistory
    ADD CONSTRAINT cine_verse_watchhistory_user_id_movie_id_e7bc2c96_uniq UNIQUE (user_id, movie_id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: cine_verse_genre_slug_86cbb62f_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX cine_verse_genre_slug_86cbb62f_like ON public.cine_verse_genre USING btree (slug varchar_pattern_ops);


--
-- Name: cine_verse_movie_genres_genre_id_b380ec4e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX cine_verse_movie_genres_genre_id_b380ec4e ON public.cine_verse_movie_genres USING btree (genre_id);


--
-- Name: cine_verse_movie_genres_movie_id_93858df4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX cine_verse_movie_genres_movie_id_93858df4 ON public.cine_verse_movie_genres USING btree (movie_id);


--
-- Name: cine_verse_userprofile_favorite_genres_genre_id_eafe4b19; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX cine_verse_userprofile_favorite_genres_genre_id_eafe4b19 ON public.cine_verse_userprofile_favorite_genres USING btree (genre_id);


--
-- Name: cine_verse_userprofile_favorite_genres_userprofile_id_c87cacd0; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX cine_verse_userprofile_favorite_genres_userprofile_id_c87cacd0 ON public.cine_verse_userprofile_favorite_genres USING btree (userprofile_id);


--
-- Name: cine_verse_userprofile_favorites_movie_id_ab61c4f1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX cine_verse_userprofile_favorites_movie_id_ab61c4f1 ON public.cine_verse_userprofile_favorites USING btree (movie_id);


--
-- Name: cine_verse_userprofile_favorites_userprofile_id_91062bbf; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX cine_verse_userprofile_favorites_userprofile_id_91062bbf ON public.cine_verse_userprofile_favorites USING btree (userprofile_id);


--
-- Name: cine_verse_userprofile_watchlist_movie_id_e2741fdf; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX cine_verse_userprofile_watchlist_movie_id_e2741fdf ON public.cine_verse_userprofile_watchlist USING btree (movie_id);


--
-- Name: cine_verse_userprofile_watchlist_userprofile_id_87ccd15e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX cine_verse_userprofile_watchlist_userprofile_id_87ccd15e ON public.cine_verse_userprofile_watchlist USING btree (userprofile_id);


--
-- Name: cine_verse_watchhistory_movie_id_a6d3ccb0; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX cine_verse_watchhistory_movie_id_a6d3ccb0 ON public.cine_verse_watchhistory USING btree (movie_id);


--
-- Name: cine_verse_watchhistory_user_id_68f3f5d3; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX cine_verse_watchhistory_user_id_68f3f5d3 ON public.cine_verse_watchhistory USING btree (user_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cine_verse_movie_genres cine_verse_movie_gen_genre_id_b380ec4e_fk_cine_vers; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cine_verse_movie_genres
    ADD CONSTRAINT cine_verse_movie_gen_genre_id_b380ec4e_fk_cine_vers FOREIGN KEY (genre_id) REFERENCES public.cine_verse_genre(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cine_verse_movie_genres cine_verse_movie_gen_movie_id_93858df4_fk_cine_vers; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cine_verse_movie_genres
    ADD CONSTRAINT cine_verse_movie_gen_movie_id_93858df4_fk_cine_vers FOREIGN KEY (movie_id) REFERENCES public.cine_verse_movie(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cine_verse_userprofile_favorite_genres cine_verse_userprofi_genre_id_eafe4b19_fk_cine_vers; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cine_verse_userprofile_favorite_genres
    ADD CONSTRAINT cine_verse_userprofi_genre_id_eafe4b19_fk_cine_vers FOREIGN KEY (genre_id) REFERENCES public.cine_verse_genre(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cine_verse_userprofile_favorites cine_verse_userprofi_movie_id_ab61c4f1_fk_cine_vers; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cine_verse_userprofile_favorites
    ADD CONSTRAINT cine_verse_userprofi_movie_id_ab61c4f1_fk_cine_vers FOREIGN KEY (movie_id) REFERENCES public.cine_verse_movie(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cine_verse_userprofile_watchlist cine_verse_userprofi_movie_id_e2741fdf_fk_cine_vers; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cine_verse_userprofile_watchlist
    ADD CONSTRAINT cine_verse_userprofi_movie_id_e2741fdf_fk_cine_vers FOREIGN KEY (movie_id) REFERENCES public.cine_verse_movie(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cine_verse_userprofile_watchlist cine_verse_userprofi_userprofile_id_87ccd15e_fk_cine_vers; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cine_verse_userprofile_watchlist
    ADD CONSTRAINT cine_verse_userprofi_userprofile_id_87ccd15e_fk_cine_vers FOREIGN KEY (userprofile_id) REFERENCES public.cine_verse_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cine_verse_userprofile_favorites cine_verse_userprofi_userprofile_id_91062bbf_fk_cine_vers; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cine_verse_userprofile_favorites
    ADD CONSTRAINT cine_verse_userprofi_userprofile_id_91062bbf_fk_cine_vers FOREIGN KEY (userprofile_id) REFERENCES public.cine_verse_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cine_verse_userprofile_favorite_genres cine_verse_userprofi_userprofile_id_c87cacd0_fk_cine_vers; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cine_verse_userprofile_favorite_genres
    ADD CONSTRAINT cine_verse_userprofi_userprofile_id_c87cacd0_fk_cine_vers FOREIGN KEY (userprofile_id) REFERENCES public.cine_verse_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cine_verse_userprofile cine_verse_userprofile_user_id_a771f7ab_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cine_verse_userprofile
    ADD CONSTRAINT cine_verse_userprofile_user_id_a771f7ab_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cine_verse_watchhistory cine_verse_watchhist_movie_id_a6d3ccb0_fk_cine_vers; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cine_verse_watchhistory
    ADD CONSTRAINT cine_verse_watchhist_movie_id_a6d3ccb0_fk_cine_vers FOREIGN KEY (movie_id) REFERENCES public.cine_verse_movie(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cine_verse_watchhistory cine_verse_watchhistory_user_id_68f3f5d3_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cine_verse_watchhistory
    ADD CONSTRAINT cine_verse_watchhistory_user_id_68f3f5d3_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

\unrestrict maHUPDRwfzAVTX7EJIWH0hRbTZmgJxNsdiDVolrnUzWe2Y25sVNusVFId8qQh2a

