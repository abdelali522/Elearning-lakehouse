SELECT
    id_assessment                       AS assessment_id,
    code_module                         AS module_code,
    code_presentation                   AS presentation_code,
    assessment_type                     AS assessment_type,
    CAST(date AS INT)                   AS due_date,
    CAST(weight AS FLOAT)               AS weight
FROM {{ source('oulad', 'assessments') }}