SELECT
    id_student                          AS student_id,
    code_module                         AS module_code,
    code_presentation                   AS presentation_code,
    gender                              AS gender,
    region                              AS region,
    highest_education                   AS highest_education,
    imd_band                            AS imd_band,
    age_band                            AS age_band,
    CAST(num_of_prev_attempts AS INT)   AS prev_attempts,
    CAST(studied_credits AS INT)        AS studied_credits,
    disability                          AS disability,
    final_result                        AS final_result
FROM {{ source('oulad', 'studentInfo') }}