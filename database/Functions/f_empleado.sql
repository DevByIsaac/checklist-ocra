CREATE OR REPLACE FUNCTION insert_employee(
     p_rol VARCHAR,
     p_nombre VARCHAR,
     p_apellido VARCHAR,
     p_sexo VARCHAR,
     p_edad INTEGER,
     p_puesto VARCHAR,
     p_duracion_turno INTEGER,
     p_duracion_descanso INTEGER,
     p_duracion_tiempo_libre INTEGER,
     p_created_by VARCHAR,
     p_updated_by VARCHAR
) RETURNS INTEGER AS $$
DECLARE
    new_employee_id INTEGER;
BEGIN
    -- Insert a new employee into the Employee table
    INSERT INTO Empleado (rol, Nombre, Apellido, sexo, edad, puesto, duracion_turno, duracion_descanso, duracion_tiempo_libre, created_by, updated_by)
    VALUES (p_rol, p_nombre, p_apellido, p_sexo, p_edad, p_puesto, p_duracion_turno, p_duracion_descanso, p_duracion_tiempo_libre, p_created_by, p_updated_by)
    RETURNING empleado_id INTO new_employee_id;

    -- Return the ID of the new employee
    RETURN new_employee_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION public.get_empleado_by_id(
    p_empleado_id INTEGER)
RETURNS TABLE(
    empleado_id INTEGER,
    rol VARCHAR,
    Nombre VARCHAR,
    Apellido VARCHAR,
    sexo VARCHAR,
    edad INTEGER,
    puesto VARCHAR,
    duracion_turno INTEGER,
    duracion_descanso INTEGER,
    duracion_tiempo_libre INTEGER,
    created_by VARCHAR,
    updated_by VARCHAR)
LANGUAGE 'plpgsql'
AS $$
BEGIN
    RETURN QUERY
    SELECT empleado_id, rol, Nombre, Apellido, sexo, edad, puesto, duracion_turno, duracion_descanso, duracion_tiempo_libre, created_by, updated_by
    FROM Empleado
    WHERE empleado_id = p_empleado_id;
END;
$$;
CREATE OR REPLACE FUNCTION public.get_all_empleados()
RETURNS TABLE(
    empleado_id INTEGER,
    rol VARCHAR,
    Nombre VARCHAR,
    Apellido VARCHAR,
    sexo VARCHAR,
    edad INTEGER,
    puesto VARCHAR,
    duracion_turno INTEGER,
    duracion_descanso INTEGER,
    duracion_tiempo_libre INTEGER,
    created_by VARCHAR,
    updated_by VARCHAR)
LANGUAGE 'plpgsql'
AS $$
BEGIN
    RETURN QUERY
    SELECT empleado_id, rol, Nombre, Apellido, sexo, edad, puesto, duracion_turno, duracion_descanso, duracion_tiempo_libre, created_by, updated_by
    FROM Empleado;
END;
$$;
