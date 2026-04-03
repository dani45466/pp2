-- 1. Процедура insert/update одного контакта
CREATE OR REPLACE PROCEDURE upsert_contact(
    p_name VARCHAR,
    p_surname VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Проверка телефона
    IF p_phone !~ '^\+?[0-9]{10,15}$' THEN
        RAISE EXCEPTION 'Invalid phone format: %', p_phone;
    END IF;

    IF EXISTS (
        SELECT 1
        FROM contacts
        WHERE name = p_name
          AND COALESCE(surname, '') = COALESCE(p_surname, '')
    ) THEN
        UPDATE contacts
        SET phone = p_phone
        WHERE name = p_name
          AND COALESCE(surname, '') = COALESCE(p_surname, '');
    ELSE
        INSERT INTO contacts(name, surname, phone)
        VALUES (p_name, p_surname, p_phone);
    END IF;
END;
$$;


-- 2. Процедура bulk insert/update
-- Для простоты принимаем 3 массива одинаковой длины
-- Некорректные записи собираем в temporary table invalid_contacts
CREATE OR REPLACE PROCEDURE upsert_many_contacts(
    p_names TEXT[],
    p_surnames TEXT[],
    p_phones TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
    arr_len INT;
BEGIN
    arr_len := array_length(p_names, 1);

    IF arr_len IS NULL THEN
        RAISE NOTICE 'Empty input arrays';
        RETURN;
    END IF;

    IF arr_len <> array_length(p_surnames, 1)
       OR arr_len <> array_length(p_phones, 1) THEN
        RAISE EXCEPTION 'Arrays must have the same length';
    END IF;

    -- временная таблица для неверных данных
    CREATE TEMP TABLE IF NOT EXISTS invalid_contacts (
        name TEXT,
        surname TEXT,
        phone TEXT,
        reason TEXT
    ) ON COMMIT DROP;

    -- очищаем, если была раньше в этой сессии
    DELETE FROM invalid_contacts;

    FOR i IN 1..arr_len LOOP
        -- Проверяем имя
        IF p_names[i] IS NULL OR btrim(p_names[i]) = '' THEN
            INSERT INTO invalid_contacts(name, surname, phone, reason)
            VALUES (p_names[i], p_surnames[i], p_phones[i], 'Invalid name');

        -- Проверяем телефон
        ELSIF p_phones[i] IS NULL OR p_phones[i] !~ '^\+?[0-9]{10,15}$' THEN
            INSERT INTO invalid_contacts(name, surname, phone, reason)
            VALUES (p_names[i], p_surnames[i], p_phones[i], 'Invalid phone');

        ELSE
            -- upsert логика
            IF EXISTS (
                SELECT 1
                FROM contacts
                WHERE name = p_names[i]
                  AND COALESCE(surname, '') = COALESCE(p_surnames[i], '')
            ) THEN
                UPDATE contacts
                SET phone = p_phones[i]
                WHERE name = p_names[i]
                  AND COALESCE(surname, '') = COALESCE(p_surnames[i], '');
            ELSE
                INSERT INTO contacts(name, surname, phone)
                VALUES (p_names[i], p_surnames[i], p_phones[i]);
            END IF;
        END IF;
    END LOOP;

    RAISE NOTICE 'Bulk operation finished. To see invalid rows run: SELECT * FROM invalid_contacts;';
END;
$$;


-- 3. Процедура удаления по username или phone
CREATE OR REPLACE PROCEDURE delete_contact(p_value TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM contacts
    WHERE name = p_value
       OR phone = p_value;
END;
$$;