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

set @v_usd_delta = 999;
select id, dt_updated, liq_usd, liq_usd_delta, tok_name, tok_symb, pair_tok_symb, pair_tok_name, 
		pair_addr, tok_addr, pair_tok_type, pair_tok_addr 
	from log_token_pairs 
	where (liq_usd_delta < -@v_usd_delta or @v_usd_delta < liq_usd_delta)															
		and (tok_addr != '0xCc78A0acDF847A2C1714D2A925bB4477df5d48a6' -- Atropa
			and pair_tok_addr != '0x6B175474E89094C44Da98b954EedeAC495271d0F') -- pDAI
		and (tok_addr != '0xA1077a294dDE1B09bB078844df40758a5D0f9a27' -- WPLS
			and pair_tok_addr != '0x95B303987A60C71504D99Aa1b13B4DA07b0790ab') -- PLSX
	order by liq_usd_delta, dt_updated, pair_addr  desc;

-- 0xA1077a294dDE1B09bB078844df40758a5D0f9a27
-- 0xCc78A0acDF847A2C1714D2A925bB4477df5d48a6
-- #============= COMMON - log_token_pairs =============#



-- #============ COMMON log_irc ============#

-- check server status
select * from log_irc order by id desc;

-- trying to find maria msgs about tokens with ' . '  in name
-- select id, time_parse, channel, usr_parse, msg_parse from log_irc 
-- 	where id <= 6189 + 10 and id >= 6189 - 10
-- 	order by time_parse asc;

-- select id, time_parse, channel, usr_parse, msg_parse from log_irc 
-- 	where msg_parse like '% .%'
-- 		and usr_parse like '%maria%'
-- 	order by time_parse asc;

-- get latest #atropa_logged (by limit)
select * from log_irc where channel = '#atropa_logged' order by time_parse desc limit 50;
select id, time_parse, channel, usr_parse, msg_parse from log_irc 
	where channel = '#atropa' 
		and msg_parse != 'nil_parse'
	order by time_parse desc limit 100;

-- get latest #atropa (by limit)
select * from log_irc where channel = '#atropa' order by time_parse desc limit 50;
select id, time_parse, channel, usr_parse, msg_parse from log_irc 
	where channel = '#atropa' 
		and msg_parse != 'nil_parse'
	order by time_parse desc limit 100;

-- get latest #pulsechain (by limit)
select * from log_irc where channel = '#pulsechain' order by time_parse desc limit 50;
select id, time_parse, channel, usr_parse, msg_parse from log_irc 
	where channel = '#pulsechain'
		and msg_parse != 'nil_parse'
	order by time_parse desc limit 200;

-- get latest #pulsechain msgs (by time)
set @last_id = 5789;
set @dt_last = '2023-10-15 05:58:35.35';
select id, time_parse, channel, usr_parse, msg_parse from log_irc 
	where time_parse >= @dt_last
		and channel = '#pulsechain'
		and msg_parse != 'nil_parse'
	order by time_parse asc;

-- get latest #atropa msgs (by time)
set @dt_last = '2023-10-12 18:24:06';
select id, time_parse, channel, usr_parse, msg_parse from log_irc 
	where time_parse >= @dt_last
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
	order by time_parse asc;

-- search maria, rh, 007 (w/ tsfi in msg_parse)
select id, time_parse, channel, usr_parse, msg_parse from log_irc 
	where id >= 0 and
		(usr_parse like '%maria%'
		or usr_parse like '%big%' 
		or usr_parse like '%007%')
		and msg_parse like '%tsfi%'
	order by time_parse asc;

select id, time_parse, channel, usr_parse, msg_parse from log_irc 
	where id > 5789 and channel = '#atropa'
	order by time_parse asc;

-- get all
select * from log_irc order by time_parse desc;

-- search IP address
select time_parse, channel, usr_parse, msg_parse, usr_loc_parse from log_irc 
	where usr_loc_parse like '%146.70.183.19%'
	order by time_parse desc;

-- #============ COMMON log_irc ============#

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


-- #============ COMMON log_irc ============#


