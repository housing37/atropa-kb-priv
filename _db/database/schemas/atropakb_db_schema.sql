#===============================================#
# init database 'atropa_kb'
#===============================================#
-- drop if exists database atropa_kb;
-- create database atropa_kb;
-- use atropa_kb;

#===============================================#
# clean
#===============================================#
-- call DeleteAll_IF_EXISTS('client_shops', 'password37', @result);

#===============================================#
# active / live
#===============================================#
-- {'tok_addr': '0xd6c31bA0754C4383A41c0e9DF042C62b5e918f6d', 'pair_addr': '0xa511e25274857344b53811DE5466039365Ca6Be1', 'liq': 23586.18, 'pr_QT': '218373.43', 'tok_symb': 'TEDDY BEAR ㉾', 'tok_name': 'BEAR', 'pulsex': 'v1'}
drop table if exists log_liq;
CREATE TABLE `log_liq` (
  -- added: 101023
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dt_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_deleted` timestamp NULL DEFAULT NULL,
  `chain_id` varchar(255) NOT NULL, -- dexscreener api: 'chanId'
  `bt_name` varchar(255) NOT NULL, -- dexscreener api: 'baseToken' 'name'
  `bt_symb` varchar(255) NOT NULL, -- dexscreener api: 'baseToken' 'symbol'
  `bt_addr` varchar(255) NOT NULL, -- dexscreener api: 'baseToken' 'addr'
  `qt_name` varchar(255) NOT NULL, -- dexscreener api: 'quoteToken' 'name'
  `qt_symb` varchar(255) NOT NULL, -- dexscreener api: 'quoteToken' 'symbol'
  `qt_addr` varchar(255) NOT NULL, -- dexscreener api: 'quoteToken' 'addr'
  `pair_addr` varchar(255) NOT NULL, -- dexscreener api: 'pairAddress'
  `liq_usd` varchar(32) NOT NULL, -- dexscreener api: 'liquidity' 'usd'
  `price_usd` varchar(32) NOT NULL, -- dexscreener api: 'priceUsd'
  `dex_name` varchar(64) NOT NULL, -- dexscreener api: 'dexId'
  `dex_vers` varchar(10) NOT NULL, -- dexscreener api: 'labels[0]'
  UNIQUE KEY `ID` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- #send_to_db(data, str_print, str_time, usr, msg, server, port, nick, channel)
drop table if exists log_irc;
CREATE TABLE `log_irc` (
  -- added: 101023
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dt_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_deleted` timestamp NULL DEFAULT NULL,
  `server` varchar(255) NOT NULL, -- server
  `port` varchar(255) NOT NULL, -- port
  `nick_log` varchar(255) NOT NULL, -- nick
  `channel` varchar(255) NOT NULL, -- channel
  `str_print` TEXT NOT NULL, -- str_print
  `time_parse` varchar(255) DEFAULT 'nil_parse', -- str_time
  `usr_parse` varchar(255) DEFAULT 'nil_parse', -- usr
  `msg_parse` varchar(1024) DEFAULT NULL, -- msg
  `raw_data` TEXT NOT NULL, -- data
  UNIQUE KEY `ID` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

#===============================================#
# legacy
#===============================================#
drop table if exists valid_employees;
CREATE TABLE `valid_employees` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `emp_name` varchar(255) NOT NULL,
  `emp_email_1` varchar(255) DEFAULT NULL,
  `emp_email_2` varchar(255) DEFAULT NULL,
  `emp_phone_1` varchar(255) DEFAULT NULL,
  `emp_phone_2` varchar(255) DEFAULT NULL,
  `code_post_job` varchar(40) DEFAULT NULL,
  `code_post_cand` varchar(40) DEFAULT NULL,
  `dt_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY `ID` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

drop table if exists valid_pins;
CREATE TABLE `valid_pins` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fk_emp_id` int(11) NOT NULL,
  `pin` varchar(40) NOT NULL,
  `dt_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY `ID` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

#===============================================#
#===============================================#
