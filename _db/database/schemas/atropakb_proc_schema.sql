DELIMITER $$
drop PROCEDURE if exists liq_ADD_LOG;
CREATE PROCEDURE `liq_ADD_LOG`(
    IN p_chain_id VARCHAR(255),
    IN p_bt_name VARCHAR(255),
    IN p_bt_symb VARCHAR(255),
    IN p_bt_addr VARCHAR(255),
    IN p_qt_name VARCHAR(255),
    IN p_qt_symb VARCHAR(255),
    IN p_qt_addr VARCHAR(255),
    IN p_pair_addr VARCHAR(255),
    IN p_liq_usd VARCHAR(32),
    IN p_price_usd VARCHAR(32),
    IN p_dex_name VARCHAR(64),
    IN p_dex_vers VARCHAR(10)
BEGIN
	-- add event log
	INSERT INTO log_liquidity (
            chain_id,
            bt_name,
            bt_symb,
            bt_addr,
            qt_name,
            qt_symb,
            qt_addr,
            pair_addr,
            liq_usd,
            price_usd,
            dex_name,
            dex_vers
		) VALUES (
            p_chain_id,
            p_bt_name,
            p_bt_symb,
            p_bt_addr,
            p_qt_name,
            p_qt_symb,
            p_qt_addr,
            p_pair_addr,
            p_liq_usd,
            p_price_usd,
            p_dex_name,
            p_dex_vers
		);

	-- RETURN
	SELECT LAST_INSERT_ID() into @new_log_id;
	SELECT dt_updated,
				'success' as `status`,
				'added new liquidity event log' as info,
				@new_log_id as new_log_id,
				p_pair_addr as pair_addr,
                p_bt_addr as bt_addr
		FROM log_liq
		WHERE id = @new_log_id;
END $$
DELIMITER ;

DELIMITER $$
drop PROCEDURE if exists irc_ADD_LOG;
CREATE PROCEDURE `irc_ADD_LOG`(
    IN p_raw_data BLOB,
    IN p_str_print BLOB,
    IN p_time_parse VARCHAR(255),
    IN p_usr_parse VARCHAR(255),
    IN p_msg_parse BLOB,
    IN p_server VARCHAR(255),
    IN p_port VARCHAR(255),
    IN p_nick_log VARCHAR(255),
    IN p_channel VARCHAR(255)
BEGIN
	-- add event log
	INSERT INTO log_irc (
            raw_data,
            str_print,
            time_parse,
            usr_parse,
            msg_parse,
            server,
            port,
            nick_log,
            channel
		) VALUES (
            p_raw_data,
            p_str_print,
            p_time_parse,
            p_usr_parse,
            p_msg_parse,
            p_server,
            p_port,
            p_nick_log,
            p_channel
		);

	-- RETURN
	SELECT LAST_INSERT_ID() into @new_log_id;
	SELECT dt_updated,
				'success' as `status`,
				'added new irc event log' as info,
				@new_log_id as new_log_id,
				p_usr_parse as usr_logged
		FROM log_irc
		WHERE id = @new_log_id;
END $$
DELIMITER ;

DELIMITER $$
drop PROCEDURE if exists ValidatePIN; -- setup
CREATE PROCEDURE `ValidatePIN` (IN p_PIN VARCHAR(40), OUT p_Result INT)
BEGIN
	-- returns 1  (if PIN is valid and active)
	-- returns 0  (if PIN is invalid and old)
	-- returns -1 (if PIN is invalid and never used)
	
	DECLARE v_validPIN INT;
	DECLARE v_inputPIN INT;
	DECLARE v_2 INT;
	DECLARE v_authPIN INT;
	SELECT GetEmpIDFrom_PIN(p_PIN) INTO v_validPIN;
	IF v_validPIN > 0 THEN
		SELECT id FROM valid_pins WHERE BINARY pin = BINARY p_PIN ORDER BY id DESC LIMIT 1 INTO v_inputPIN;
		SELECT fk_emp_id FROM valid_pins WHERE BINARY pin = BINARY p_PIN ORDER BY id DESC LIMIT 1 INTO v_2;
		SELECT id FROM valid_pins WHERE fk_emp_id = v_2 ORDER BY id DESC LIMIT 1 INTO v_authPIN;
		SELECT v_inputPIN = v_authPIN INTO p_Result;
	ELSE
		SELECT v_validPIN INTO p_Result;
	END IF;
END
$$ DELIMITER ;

DELIMITER $$
drop FUNCTION if exists GetEmpIDFrom_PIN; -- setup
CREATE FUNCTION `GetEmpIDFrom_PIN`(p_PIN VARCHAR(40)) RETURNS INT(11)
    READS SQL DATA
    DETERMINISTIC
Begin
	-- returns emp ID that last used this PIN
	-- returns -1 if PIN was never valid/used
	
	DECLARE v_i INT;
	SELECT fk_emp_id FROM valid_pins WHERE BINARY pin = BINARY p_PIN ORDER BY id DESC LIMIT 1 INTO v_i;
	IF v_i IS NULL THEN
		RETURN -1;
	ELSE
		RETURN v_i;
	END IF;
END
$$ DELIMITER ;


-- DELIMITER $$
-- drop PROCEDURE if exists avm_GET_EVT_CODE_LOG; -- setup
-- CREATE PROCEDURE `avm_GET_EVT_CODE_LOG`(
-- 	IN p_evt_code VARCHAR(40),
-- 	IN p_get_default boolean)
-- BEGIN
-- 	if p_get_default then
-- 		select DATE_SUB(dt_updated, INTERVAL 4 HOUR) AS `date_est`,
-- 				evt_code,
-- 				evt_descr,
-- 				evt_level
-- 			from avm_logs
-- 			where evt_code = 'S'
-- 				or evt_code = 'K'
-- 				or (evt_code = 'V' and evt_level > -1)
-- 			order by `date_est` desc;
-- 	else
-- 		select DATE_SUB(dt_updated, INTERVAL 4 HOUR) AS `date_est`,
-- 				evt_code,
-- 				evt_descr,
-- 				evt_level
-- 			from avm_logs
-- 			where (evt_code = p_evt_code and evt_level > -1)
-- 			order by `date_est` desc;
-- 	end if;

-- END
-- $$ DELIMITER ;

-- DELIMITER $$
-- drop PROCEDURE if exists AVM_GET_CNT_DT_EVT_TYPE; -- setup
-- CREATE PROCEDURE `AVM_GET_CNT_DT_EVT_TYPE`(
-- 	IN p_dt_updated VARCHAR(40),
-- 	IN p_evt_type VARCHAR(10))
-- BEGIN
-- 	SELECT count(*)
-- 		FROM avm_logs
-- 		INTO @v_count;

-- 	IF @v_count > 0 THEN
-- 		-- 	GET FROM X TIME TO X TIME
-- 		-- SELECT CONCAT(p_dt_updated, " 03:00:00") INTO @v_dt_utc_start;
--         SELECT CONCAT(p_dt_updated, " 05:00:00") INTO @v_dt_utc_start;
-- 		-- SELECT DATE_ADD(@v_dt_utc_start, INTERVAL 4 HOUR) INTO @v_dt_edt_start;
-- 		SELECT DATE_ADD(@v_dt_utc_start, INTERVAL 5 HOUR) INTO @v_dt_edt_start; -- EST
-- 		SELECT DATE_ADD(@v_dt_edt_start, INTERVAL 1 DAY) INTO @v_dt_edt_end;
-- 		SELECT dt_updated, count(*) as 'evt_type count',
-- 				p_evt_type as input_evt_type,
-- 				'success' as `status`,
-- 				'retrieved avm_log count for dt_updated & evt_type' as info,
-- 				p_dt_updated as input_dt_updated
-- 			FROM avm_logs
-- 			WHERE evt_code = p_evt_type
-- 				AND dt_updated
-- 					BETWEEN @v_dt_edt_start AND @v_dt_edt_end
-- 				ORDER BY dt_updated DESC;
-- 	ELSE
-- 		SELECT 'failed' as `status`,
-- 				'no avm_logs found at all' as info,
-- 				p_dt_updated as input_dt_updated,
-- 				p_evt_type as input_evt_type;
-- 	END IF;
-- END
-- $$ DELIMITER ;
