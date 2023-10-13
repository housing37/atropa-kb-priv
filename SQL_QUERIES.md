-- #============= COMMON - log_token_pairs =============#
select * from log_token_pairs;
select id, liq_usd, liq_usd_delta, pair_addr, tok_addr, pair_tok_type, pair_tok_addr from log_token_pairs order by pair_addr;
select id, liq_usd, liq_usd_delta, pair_addr, tok_addr, pair_tok_type, pair_tok_addr from log_token_pairs order by liq_usd_delta desc;
select id, liq_usd, liq_usd_delta, pair_addr, tok_addr, pair_tok_type, pair_tok_addr from log_token_pairs order by id desc;
select id, dt_updated, liq_usd, liq_usd_delta, tok_name, pair_tok_name, pair_addr, tok_addr, pair_tok_type, pair_tok_addr 
	from log_token_pairs 
	where pair_addr = '0x0a022e7591749B0ed0D9e3b7B978f26978440DC7'
	order by pair_addr, dt_updated desc;

select id, dt_updated, liq_usd, liq_usd_delta, tok_name, pair_tok_name, pair_addr, tok_addr, pair_tok_type, pair_tok_addr 
	from log_token_pairs 
	where pair_tok_name = 'TSFi'
	order by pair_addr, dt_updated desc;

select id, dt_updated, liq_usd, liq_usd_delta, tok_name, pair_tok_name, pair_addr, tok_addr, pair_tok_type, pair_tok_addr 
	from log_token_pairs 
	where tok_name = 'Atropa'
	order by pair_addr, dt_updated desc;

select id, dt_updated, liq_usd, liq_usd_delta, tok_name, pair_tok_name, pair_addr, tok_addr, pair_tok_type, pair_tok_addr 
	from log_token_pairs 
	where pair_tok_name = 'TSFi'
	order by pair_addr, dt_updated desc;
-- #============= COMMON - log_token_pairs =============#


-- #============ COMMON - log_irc ============#

-- get latest #pulsechain
set @last_id = 5789;
set @dt_last = '2023-10-11 18:24:06';
select id, time_parse, channel, usr_parse, msg_parse from log_irc 
	where time_parse >= @dt_last
-- 	where id >= @last_id
		and channel = '#pulsechain'
		and msg_parse != 'nil_parse'
	order by time_parse asc;

-- get latest #atropa
set @dt_last = '2023-10-12 18:24:06';
select id, time_parse, channel, usr_parse, msg_parse from log_irc 
	where time_parse >= @dt_last
-- 	where id >= 5789
		and channel = '#atropa'
		and msg_parse != 'nil_parse'
	order by time_parse asc;

-- get all (msgs only)
select time_parse, channel, usr_parse, msg_parse, str_print, raw_data 
	from log_irc 
	where msg_parse != 'nil_parse' 
	order by time_parse desc;

-- get all organized
select time_parse, channel, usr_parse, msg_parse, str_print, raw_data from log_irc order by time_parse desc;

-- search maria, rh, 007
select id, time_parse, channel, usr_parse, msg_parse from log_irc 
	where id >= 5789 and
		(usr_parse like '%maria%'
		or usr_parse like '%big%' 
		or usr_parse like '%007%')
	order by time_parse desc;
-- 	order by time_parse asc;

select id, time_parse, channel, usr_parse, msg_parse from log_irc 
	where id > 5789 and channel = '#atropa'
-- 	order by time_parse desc;
	order by time_parse asc;

-- get all
select * from log_irc order by time_parse desc;

-- search IP address
select time_parse, channel, usr_parse, msg_parse, usr_loc_parse from log_irc 
	where usr_loc_parse like '%146.70.183.19%'
	order by time_parse desc;

-- #============ COMMON - log_irc ============#

select `server`, `port`, time_parse, channel, usr_parse, msg_parse, str_print from log_irc order by time_parse desc;
select nick_log, time_parse, channel, usr_parse, msg_parse, str_print from log_irc order by time_parse desc;

select `server`, `port`, channel, dt_created, time_parse, usr_parse, msg_parse from log_irc order by time_parse DESC;
select dt_updated, usr_parse, msg_parse from log_irc order by dt_updated desc;
select str_print from log_irc order by id desc;
select raw_data from log_irc order by id desc;
select * from log_irc order by id desc;

select usr_loc_parse, raw_data from log_irc order by id desc;

-- delete from log_irc;

select nick_log, dt_updated, time_parse, channel, usr_parse, msg_parse, str_print, raw_data 
from log_irc 
where nick_log = 'hlog_import'
order by time_parse desc;

select nick_log, dt_updated, time_parse, channel, usr_parse, msg_parse, str_print, raw_data from log_irc order by time_parse desc;
select * from log_irc where usr_parse = 'jack_';

select time_parse, usr_parse, msg_parse from log_irc where raw_data like '%mariarahel%' order by time_parse desc;


