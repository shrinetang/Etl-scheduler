--
-- 数据库: `rp_ud_etl`
--
CREATE DATABASE IF NOT EXISTS rp_ud_etl default charset utf8 COLLATE utf8_general_ci;
USE rp_ud_etl;


--
-- 表结构 `tbl_run_macheine_info`
--
CREATE TABLE IF NOT EXISTS `tbl_run_macheine_info`(
    `id`            int           NOT NULL AUTO_INCREMENT,
    `machine`       varchar(128)  NOT NULL DEFAULT '',
    `port`          int           NOT NULL DEFAULT 8963,
    `tasks`         int           NOT NULL DEFAULT 100,
    `status`        varchar(16)   NOT NULL DEFAULT '',

    PRIMARY KEY (`id`)
) ENGINE=innoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;


--
-- 表结构 `tbl_run_macheine_status`
--
CREATE TABLE IF NOT EXISTS `tbl_run_macheine_info`(
    `id`            int           NOT NULL AUTO_INCREMENT,
    `machine`       varchar(128)  NOT NULL DEFAULT '',
    `port`          int           NOT NULL DEFAULT 8963,
    `task_id`       varchar(64)   NOT NULL DEFAULT '',

    PRIMARY KEY (`id`)
) ENGINE=innoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;
