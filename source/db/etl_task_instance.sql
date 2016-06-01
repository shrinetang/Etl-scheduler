--
-- 数据库: `rp_ud_etl`
--
CREATE DATABASE IF NOT EXISTS rp_ud_etl default charset utf8 COLLATE utf8_general_ci;
USE rp_ud_etl;

--
-- 表结构 `tbl_task_instance_info`
--
CREATE TABLE IF NOT EXISTS `tbl_task_instance_info`(
    `id`                     int           NOT NULL AUTO_INCREMENT,
    `stream_id`              int           NOT NULL DEFAULT 0,
    `stream_instance_id`     int           NOT NULL DEFAULT 0,
    `task_name`              varchar(128)  NOT NULL DEFAULT '',
    `instance_id`            varchar(64)   NOT NULL DEFAULT '',
    `depend_idlist`          varchar(1024) NOT NULL DEFAULT '',
    `config`                 varchar(8192) NOT NULL DEFAULT '',
    `crontab`                varchar(32)   NOT NULL DEFAULT '',
    `ctime`                  datetime      NOT NULL DEFAULT 0,
    `work_machine`           varchar(64)   NOT NULL DEFAULT '',
    `queue`                  datetime      NOT NULL DEFAULT 0,
    `start`                  datetime      NOT NULL DEFAULT 0,
    `finish`                 datetime      NOT NULL DEFAULT 0,
    `cur_retry`              int           NOT NULL DEFAULT 0,
    `cur_alarm_repeat`       int           NOT NULL DEFAULT 0,
    `datasize`               bigint        NOT NULL DEFAULT 0,
    `dataline`               bigint        NOT NULL DEFAULT 0,
    `version`                int           NOT NULL DEFAULT 0,
    `status`                 varchar(16)   NOT NULL DEFAULT '',
    `status_msg`             varchar(1024) NOT NULL DEFAULT '',

    PRIMARY KEY (`id`),
    UNIQUE  KEY `uk_stream_instance`(`stream_id`, `stream_instance_id`),
    KEY         `idx_stream_id`(`instance_id`),
    KEY         `idx_status`(`status`)
) ENGINE=innoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;
