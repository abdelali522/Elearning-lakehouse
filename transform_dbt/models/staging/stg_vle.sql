SELECT
    id_site                             AS site_id,
    code_module                         AS module_code,
    code_presentation                   AS presentation_code,
    activity_type                       AS activity_type,
    CAST(week_from AS INT)              AS week_from,
    CAST(week_to AS INT)                AS week_to
FROM {{ source('oulad', 'vle') }}