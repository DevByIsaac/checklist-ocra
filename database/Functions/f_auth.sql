CREATE OR REPLACE FUNCTION public.authenticate_user(email TEXT, password TEXT)
RETURNS TABLE(result TEXT) AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM users u
        WHERE u.email = authenticate_user.email
        AND u.password = crypt(authenticate_user.password, u.password)
    ) THEN
        result := 'success';
    ELSE
        result := 'failure';
    END IF;
     RETURN QUERY SELECT result;
END;
$$ LANGUAGE plpgsql;
