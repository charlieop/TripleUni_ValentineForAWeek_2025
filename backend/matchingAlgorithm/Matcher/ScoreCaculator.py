import numpy as np
from typing import Callable, Tuple

class CompatibilityScoreCaculator():
    """
    A class to calculate the score of a given attributes based on a given perspective.
    """
    
    @staticmethod
    def sigmoid(x: int) -> int:
        """
        A sigmoid function to be used as a nonlinear function.
        
        Args:
            x (int): The input value.
            
        Returns:
            int: The output value.
        """
        return 2 * ( 1 / (1+np.exp(-0.13*x)) ) - 1
    
    def __init__(
        self,
        base_score: int = 0,
        mbti_item_match_max_score: int = 10,
        mbti_unmatch_penalty_rate: float = 0.4,
        mbti_no_preference_score_penalty_multiplier: float = 0.2,
        
        use_nonlinear_function: bool = True,
        nonlinear_function: Callable[[int], int] = sigmoid,
        
        hobbies_basic_score: int = 9,
        hobbies_bonus_score: int = 7,
        
        questions_basic_score: int = 5,
        questions_bonus_score: int = 5,

    ):
        self.BASE_SCORE = base_score
        self.MBTI_ITEM_MATCH_MAX_SCORE = mbti_item_match_max_score
        self.MBTI_UNMATCH_PENALTY_RATE = mbti_unmatch_penalty_rate
        self.MBTI_NO_PREFERENCE_SCORE_PENALTY_MULTIPLIER = mbti_no_preference_score_penalty_multiplier
        
        self.USE_NONLINEAR_FUNCTION = use_nonlinear_function
        self.NONLINEAR_FUNCTION = nonlinear_function
        
        self.hobbies_basic_score = hobbies_basic_score
        self.hobbies_bonus_score = hobbies_bonus_score
        
        self.questions_basic_score = questions_basic_score
        self.questions_bonus_score = questions_bonus_score

    def calc(self, a, inPrespectiveOf) -> int:
        """
        Calculates the score of the given attributes based on the provided perspective.
        
        Args:
            a (dict): A dictionary containing attributes to be scored.
            inPrespectiveOf (dict): A dictionary containing the perspective's preferences.
            
        Returns:
            int: The calculated score.
        """
        if self._check_dealbreaker(a, inPrespectiveOf):
            return 0
        score = self.BASE_SCORE
        score += self._calc_mbti(a, inPrespectiveOf, self.NONLINEAR_FUNCTION if self.USE_NONLINEAR_FUNCTION else None)
        score += self._calc_hobbies(a, inPrespectiveOf)
        score += self._calc_questionnaire(a, inPrespectiveOf)
        return score


    def _check_dealbreaker(self, a, inPrespectiveOf) -> bool:
        """
        Checks if the given attributes contain any dealbreakers based on the provided perspective.

        Args:
            a (dict): A dictionary containing attributes to be checked.
            inPrespectiveOf (dict): A dictionary containing the perspective's preferences.

        Returns:
            bool: True if any dealbreaker is found, False otherwise.
        """
        if a.get("grade") not in inPrespectiveOf.get("preferred_grades"):
            return True
        if a.get("school") not in inPrespectiveOf.get("preferred_schools"):
            return True
        return False


    def _calc_mbti(self, a, inPrespectiveOf, nonlinearResampleFunction: Callable[[int], int] = None) -> int:
        """
        Calculate the MBTI compatibility score between two profiles.
        Args:
            a (dict): The MBTI profile of the first individual.
            inPrespectiveOf (dict): The MBTI preferences of the second individual.
            nonlinearResampleFunction (Callable[[int], int], optional): A function to apply a nonlinear transformation to the score. Defaults to None.
        Returns:
            int: The calculated MBTI compatibility score.
        """
        MBTI_KEYS= ["ei", "sn", "tf", "jp"]
        score = 0
        for key in MBTI_KEYS:
            a_value = a.get(f"mbti_{key}")
            pref_value = inPrespectiveOf.get(f"preferred_mbti_{key}")
            if pref_value == "x":
                score += self.MBTI_ITEM_MATCH_MAX_SCORE * self.MBTI_NO_PREFERENCE_SCORE_PENALTY_MULTIPLIER
                continue
            if pref_value == key[0]:
                x = (50 - a_value)
            else:
                x = (a_value - 50)
            
            if x < 0:
                x = x * self.MBTI_UNMATCH_PENALTY_RATE
                
            if not nonlinearResampleFunction:
                score += x / 50 * self.MBTI_ITEM_MATCH_MAX_SCORE
            else:
                score += nonlinearResampleFunction(x) * self.MBTI_ITEM_MATCH_MAX_SCORE
        return score


    def _calc_hobbies(self, a, inPrespectiveOf) -> int:
        """
        Calculate the hobby compatibility score between two individuals.

        This method compares the hobbies of two individuals and calculates a score based on the number of shared hobbies.
        Additional bonus points are awarded for specific hobbies, and penalties are applied if certain conditions are met.

        Args:
            a (dict): A dictionary representing the first individual's hobbies. Keys are expected to be in the format 'hobby1', 'hobby2', 'hobby3'.
            inPrespectiveOf (dict): A dictionary representing the second individual's hobbies. Keys are expected to be in the format 'hobby1', 'hobby2', 'hobby3'.

        Returns:
            int: The calculated hobby compatibility score.
        """
        a_hobbies = set()
        b_hobbies = set()
        for i in range(1, 4):
            a_hobby = a.get(f"hobby{i}", None)
            b_hobby = inPrespectiveOf.get(f"hobby{i}", None)
            if a_hobby:
                a_hobbies.add(a_hobby)
            if b_hobby:
                b_hobbies.add(b_hobby)
        intersection = a_hobbies.intersection(b_hobbies)
        score = len(intersection) * self.hobbies_basic_score
        MINOR_HOBBIES = ["paint", "create"]
        for hobby in MINOR_HOBBIES:
            if hobby in intersection:
                score += self.hobbies_bonus_score
        if "acg" in a_hobbies:
            if "acg" in b_hobbies:
                score += self.hobbies_bonus_score
            else:
                score -= self.hobbies_basic_score
        return score
    
    def _calc_questionnaire(self, a, inPrespectiveOf) -> int:
        """
        Calculate the matching score based on questionnaire answers.

        This method compares the answers of two participants (a and inPrespectiveOf) 
        to a predefined set of questions and calculates a score based on the 
        similarity of their answers. Additional bonus scores are awarded for 
        specific answers to certain questions.

        Args:
            a (dict): A dictionary containing the answers of the first participant.
            inPrespectiveOf (dict): A dictionary containing the answers of the second participant.

        Returns:
            int: The calculated matching score.
        """
        QUESTIONS = ["travel_destination", "superpower", "use_of_money", "family", "lifestyle"]
        score = 0
        for question in QUESTIONS:
            a_answer = a.get(question)
            b_answer = inPrespectiveOf.get(question)
            if a_answer == b_answer:
                score += self.questions_basic_score
            if question == "travel_destination" and a_answer == "none":
                if b_answer == a_answer:
                    score += self.questions_bonus_score
                else:
                    score -= self.questions_basic_score
            if question == "use_of_money" and a_answer == "charity":
                if b_answer == a_answer:
                    score += self.questions_bonus_score
            if question == "use_of_money" and a_answer == "daily":
                if b_answer == a_answer:
                    score += self.questions_bonus_score
            BONUS_LIFESTYLE = ["matrix", "jurassic", "1984"]
            if question == "lifestyle" and a_answer in BONUS_LIFESTYLE:
                if b_answer == a_answer:
                    score += self.questions_bonus_score
        return score


class ScoreMatrixCalculator():
    """
    A class to calculate the score matrix of a given DataFrame based on a given compability score calculator.
    """
    
    def __init__(self, score_calculator: CompatibilityScoreCaculator):
        """
        Initializes the ScoreMatrix object with the given score calculator.
        
        Args:
            score_calculator (CompatibilityScoreCaculator): The score calculator to be used.
        """
        self.score_calculator = score_calculator


    def get_hetrogenous_group_score_matrix(self, hetro_F, hetro_M) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculate the score matrices for heterogeneous groups.

        This method computes the score matrices between two heterogeneous groups,
        typically males and females, using a provided scoring function. It returns
        three matrices: the final score matrix, the score matrix from females to males,
        and the score matrix from males to females.

        Args:
            hetro_F (pd.DataFrame): DataFrame containing the female group.
            hetro_M (pd.DataFrame): DataFrame containing the male group.

        Returns:
            tuple: A tuple containing:
                - final_score (np.ndarray): The final score matrix calculated as the 
                  element-wise maximum of the product of the female-to-male and 
                  male-to-female score matrices.
                - score_F_to_M (np.ndarray): The score matrix from females to males.
                - score_M_to_F (np.ndarray): The score matrix from males to females.
        """
        score_F_to_M = np.zeros((len(hetro_F), len(hetro_M)))
        for i, female in hetro_F.iterrows():
            for j, male in hetro_M.iterrows():
                score_F_to_M[i, j] = self.score_calculator.calc(male, female)
        score_M_to_F = np.zeros((len(hetro_M), len(hetro_F)))
        for i, male in hetro_M.iterrows():
            for j, female in hetro_F.iterrows():
                score_M_to_F[i, j] = self.score_calculator.calc(female, male)
        # final_score = np.minimum(score_F_to_M, score_M_to_F.T)
        # final_score = np.maximum((score_F_to_M + score_M_to_F.T) / 2, 0)
        final_score = np.maximum((score_F_to_M * score_M_to_F.T).astype(int), 0)
        return final_score, score_F_to_M, score_M_to_F