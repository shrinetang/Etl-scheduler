--
-- 数据库: `rp_ud_etl`
--
CREATE DATABASE IF NOT EXISTS rp_ud_etl default charset utf8 COLLATE utf8_general_ci;
USE rp_ud_etl;

--
-- 表结构 `tbl_task_info`
--
CREATE TABLE IF NOT EXISTS `tbl_task_info`(
    `id`                     int           NOT NULL AUTO_INCREMENT,
    `stream_id`              int           NOT NULL DEFAULT 0,
    `task_name`              varchar(128)  NOT NULL DEFAULT '',
    `task_version`           int           NOT NULL DEFAULT 0,
    `desc`                   varchar(256)  NOT NULL DEFAULT '',
    `config`                 varchar(8192) NOT NULL DEFAULT '',
    `tool_name`              varchar(128)  NOT NULL DEFAULT '',
    `tool_version`           int           NOT NULL DEFAULT 0,
    `depend_task`            varchar(1024) NOT NULL DEFAULT '',
    `crontab`                varchar(32)   NOT NULL DEFAULT '',
    `timeout`                int           NOT NULL DEFAULT 1440,
    `need_retry`             int           NOT NULL DEFAULT 0,
    `retry_maxnum`           int           NOT NULL DEFAULT 0,
    `retry_interval`         int           NOT NULL DEFAULT 30,
    `expect_start`           varchar(16)   NOT NULL DEFAULT '',
    `expect_finish`          varchar(16)   NOT NULL DEFAULT '',
    `err_mail_list`          varchar(256)  NOT NULL DEFAULT '',
    `err_phone_list`         varchar(256)  NOT NULL DEFAULT '',
    `not_start_mail_list`    varchar(256)  NOT NULL DEFAULT '',
    `not_start_phone_list`   varchar(256)  NOT NULL DEFAULT '',
    `not_finish_mail_list`   varchar(256)  NOT NULL DEFAULT '',
    `not_finish_phone_list`  varchar(256)  NOT NULL DEFAULT '',
    `alarm_repeat`           int           NOT NULL DEFAULT 0,
    `alarm_interval`         int           NOT NULL DEFAULT 10,
    `callback_list`          varchar(1024) NOT NULL DEFAULT '',
    `developer`              varchar(256)  NOT NULL DEFAULT '',
    `observer`               varchar(256)  NOT NULL DEFAULT '',
    `creator`                varchar(32)   NOT NULL DEFAULT '',
    `ctime`                  datetime      NOT NULL DEFAULT 0,
    `modifier`               varchar(32)   NOT NULL DEFAULT '',
    `mtime`                  datetime      NOT NULL DEFAULT 0,
    `status`                 varchar(16)   NOT NULL DEFAULT '',

    PRIMARY KEY (`id`),
    UNIQUE  KEY `uk_task_name`(`task_name`, `task_version`),
    KEY         `idx_stream_id`(`stream_id`)
) ENGINE=innoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;
