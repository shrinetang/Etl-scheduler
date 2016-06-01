--
-- 数据库: `rp_ud_etl`
--
CREATE DATABASE IF NOT EXISTS rp_ud_etl default charset utf8 COLLATE utf8_general_ci;
USE rp_ud_etl;

--
-- 表结构 `tbl_stream_info`
--
CREATE TABLE IF NOT EXISTS `tbl_stream_info`(
    `stream_id`     int           NOT NULL AUTO_INCREMENT,
    `stream_name`   varchar(64)   NOT NULL DEFAULT '',
    `stream_type`   varchar(8)    NOT NULL DEFAULT '',
    `desc`          varchar(256)  NOT NULL DEFAULT '',
    `config`        varchar(8192) NOT NULL DEFAULT '',
    `manager`       varchar(256)  NOT NULL DEFAULT '',
    `developer`     varchar(256)  NOT NULL DEFAULT '',
    `observer`      varchar(256)  NOT NULL DEFAULT '',
    `crontab`       varchar(32)   NOT NULL DEFAULT '',
    `status`        varchar(16)   NOT NULL DEFAULT '',
    `creator`       varchar(32)   NOT NULL DEFAULT '',
    `ctime`         datetime      NOT NULL DEFAULT 0,
    `modifier`      varchar(32)   NOT NULL DEFAULT '',
    `mtime`         datetime      NOT NULL DEFAULT 0,

    PRIMARY KEY (`stream_id`),
    UNIQUE  KEY `uk_stream_and_type`(`stream_name`, `stream_type`)
) ENGINE=innoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;
