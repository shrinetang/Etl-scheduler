--
-- 数据库: `rp_ud_etl`
--
CREATE DATABASE IF NOT EXISTS rp_ud_etl default charset utf8 COLLATE utf8_general_ci;
USE rp_ud_etl;

--
-- 表结构 `tbl_tool_info`
--
CREATE TABLE IF NOT EXISTS `tbl_tool_info`(
    `id`            int           NOT NULL AUTO_INCREMENT,
    `tool_name`     varchar(64)   NOT NULL DEFAULT '',
    `tool_version`  int           NOT NULL DEFAULT 1,
    `desc`          varchar(256)  NOT NULL DEFAULT '',
    `config`        varchar(8192) NOT NULL DEFAULT '',
    `developer`     varchar(256)  NOT NULL DEFAULT '',
    `status`        varchar(16)   NOT NULL DEFAULT '',
    `creator`       varchar(32)   NOT NULL DEFAULT '',
    `ctime`         datetime      NOT NULL DEFAULT 0,
    `modifier`      varchar(32)   NOT NULL DEFAULT '',
    `mtime`         datetime      NOT NULL DEFAULT 0,

    PRIMARY KEY (`id`),
    UNIQUE  KEY `uk_name_and_version`(`tool_name`, `tool_version`)
) ENGINE=innoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;
