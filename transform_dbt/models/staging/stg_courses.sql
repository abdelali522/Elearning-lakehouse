SELECT
    code_module                                 AS module_code,
    code_presentation                           AS presentation_code,
    CAST(module_presentation_length AS INT)     AS module_length_days
FROM {{ source('oulad', 'courses') }}