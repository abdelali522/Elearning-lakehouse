SELECT
    code_module                         AS module_code,
    code_presentation                   AS presentation_code,
    id_student                          AS student_id,
    id_site                             AS site_id,
    CAST(date AS INT)                   AS activity_date,
    CAST(sum_click AS INT)              AS total_clicks
FROM {{ source('oulad', 'studentVle') }}