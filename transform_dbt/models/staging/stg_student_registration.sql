SELECT
    id_student                          AS student_id,
    code_module                         AS module_code,
    code_presentation                   AS presentation_code,
    CAST(date_registration AS INT)      AS date_registration,
    CAST(date_unregistration AS INT)    AS date_unregistration
FROM {{ source('oulad', 'studentRegistration') }}