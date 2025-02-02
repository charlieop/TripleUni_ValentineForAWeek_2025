from Matcher.Utils import separate_groups, filter_applicant, connect_db_and_get_table, reshuffle_data
from Matcher.ScoreCaculator import CompatibilityScoreCaculator, ScoreMatrixCalculator
from Matcher.Hungarian import prepareMatrix, hungarian

MYSQL_DB_PATH = "./db.sqlite3"
TABLE_NAME = "applicant"


if __name__ == '__main__':
    df = connect_db_and_get_table(MYSQL_DB_PATH, TABLE_NAME)
    df = filter_applicant(df)
    hetro_F, hetro_M, homo_F, homo_M = map(reshuffle_data, separate_groups(df))
    
    score_matrix_calculator = ScoreMatrixCalculator(CompatibilityScoreCaculator())
    
    score_matrix_hetro, score_F_to_M, score_M_to_F = score_matrix_calculator.get_hetrogenous_group_score_matrix(hetro_F, hetro_M)
    score_matrix_hetro = prepareMatrix(score_matrix_hetro)
    pairing_result = hungarian(score_matrix_hetro)
    
    failed_to_match_F = []
    failed_to_match_M = []
    
    for f, m in pairing_result:
        if score_matrix_hetro[f, m] == 0:
            continue
        