"""
재순위화 모듈
가중치를 적용하여 최종 순위 결정
"""

from typing import Dict, List, Optional, Tuple
import math

class ReRanker:
    """재순위화 클래스"""
    
    def __init__(self):
        # 재순위화 알고리즘 설정
        self.ranking_algorithms = {
            "weighted_sum": self._weighted_sum_ranking,
            "multiplicative": self._multiplicative_ranking,
            "borda_count": self._borda_count_ranking
        }
        
        print("🔄 재순위화 모듈 초기화 완료")
    
    def rerank(self, vector_results: List[Dict], dynamic_weights: Dict, 
               algorithm: str = "weighted_sum") -> List[Dict]:
        """재순위화 실행"""
        print(f"🔄 재순위화 시작 (알고리즘: {algorithm})")
        
        if not vector_results:
            print("⚠️ 재순위화할 결과가 없음")
            return []
        
        # 선택된 알고리즘으로 재순위화
        ranking_func = self.ranking_algorithms.get(algorithm, self._weighted_sum_ranking)
        reranked_results = ranking_func(vector_results, dynamic_weights)
        
        # 최종 순위 부여
        for i, result in enumerate(reranked_results):
            result["final_rank"] = i + 1
            result["ranking_algorithm"] = algorithm
        
        print(f"✅ 재순위화 완료: {len(reranked_results)}명 순위 결정")
        return reranked_results
    
    def _weighted_sum_ranking(self, results: List[Dict], weights: Dict) -> List[Dict]:
        """가중합 기반 순위화"""
        
        for result in results:
            final_score = 0.0
            
            # 기본 필드 점수 계산
            for field, weight in weights.items():
                if field != "vector_fields":
                    field_score = self._calculate_field_score(result, field)
                    final_score += field_score * weight
            
            # 벡터 필드 점수 계산
            vector_weights = weights.get("vector_fields", {})
            vector_score = self._calculate_vector_score(result, vector_weights)
            final_score += vector_score * 0.4  # 벡터 필드 전체 가중치
            
            result["final_score"] = final_score
        
        # 점수 순으로 정렬
        results.sort(key=lambda x: x["final_score"], reverse=True)
        return results
    
    def _multiplicative_ranking(self, results: List[Dict], weights: Dict) -> List[Dict]:
        """곱셈 기반 순위화 (가중 기하평균)"""
        
        for result in results:
            score_product = 1.0
            total_weight = 0.0
            
            # 기본 필드 점수
            for field, weight in weights.items():
                if field != "vector_fields":
                    field_score = self._calculate_field_score(result, field)
                    if field_score > 0:
                        score_product *= (field_score ** weight)
                        total_weight += weight
            
            # 벡터 필드 점수
            vector_weights = weights.get("vector_fields", {})
            vector_score = self._calculate_vector_score(result, vector_weights)
            if vector_score > 0:
                vector_weight = 0.4
                score_product *= (vector_score ** vector_weight)
                total_weight += vector_weight
            
            # 기하평균 계산
            if total_weight > 0:
                result["final_score"] = score_product ** (1.0 / total_weight)
            else:
                result["final_score"] = 0.0
        
        results.sort(key=lambda x: x["final_score"], reverse=True)
        return results
    
    def _borda_count_ranking(self, results: List[Dict], weights: Dict) -> List[Dict]:
        """보다 카운트 기반 순위화"""
        
        n = len(results)
        field_rankings = {}
        
        # 각 필드별로 순위 계산
        for field in weights.keys():
            if field != "vector_fields":
                # 필드 점수로 정렬
                field_sorted = sorted(results, 
                                    key=lambda x: self._calculate_field_score(x, field), 
                                    reverse=True)
                
                field_rankings[field] = {result["id"] if "id" in result else id(result): rank 
                                       for rank, result in enumerate(field_sorted)}
        
        # 벡터 필드 순위
        vector_weights = weights.get("vector_fields", {})
        vector_sorted = sorted(results,
                             key=lambda x: self._calculate_vector_score(x, vector_weights),
                             reverse=True)
        field_rankings["vector_fields"] = {result["id"] if "id" in result else id(result): rank 
                                         for rank, result in enumerate(vector_sorted)}
        
        # Borda 점수 계산
        for result in results:
            result_id = result["id"] if "id" in result else id(result)
            borda_score = 0.0
            
            for field, weight in weights.items():
                if field in field_rankings:
                    rank = field_rankings[field].get(result_id, n)
                    borda_score += (n - rank - 1) * weight
            
            result["final_score"] = borda_score
        
        results.sort(key=lambda x: x["final_score"], reverse=True)
        return results
    
    def _calculate_field_score(self, result: Dict, field: str) -> float:
        """개별 필드 점수 계산"""
        
        if field == "age":
            return self._score_age_match(result)
        elif field == "residence":
            return self._score_residence_match(result)
        elif field == "industry_domain":
            return self._score_industry_match(result)
        elif field == "specialization":
            return self._score_specialization_match(result)
        elif field == "experience_years":
            return self._score_experience_match(result)
        elif field == "talent_level":
            return self._score_talent_level_match(result)
        elif field == "skills":
            return self._score_skills_match(result)
        else:
            # 기본 점수 (payload_score 사용)
            return result.get("payload_score", 0.0)
    
    def _calculate_vector_score(self, result: Dict, vector_weights: Dict) -> float:
        """벡터 필드 종합 점수 계산"""
        
        vector_score = result.get("vector_score", 0.0)
        
        # 벡터 필드별 세부 점수가 있다면 가중합 계산
        if "vector_details" in result:
            detailed_score = 0.0
            for field, weight in vector_weights.items():
                field_score = result["vector_details"].get(field, 0.0)
                detailed_score += field_score * weight
            return detailed_score
        
        return vector_score
    
    def _score_age_match(self, result: Dict) -> float:
        """나이 매칭 점수"""
        # payload_score에서 나이 관련 점수 추출하거나 별도 계산
        return result.get("age_score", result.get("payload_score", 0.0))
    
    def _score_residence_match(self, result: Dict) -> float:
        """거주지 매칭 점수"""
        return result.get("residence_score", result.get("payload_score", 0.0))
    
    def _score_industry_match(self, result: Dict) -> float:
        """산업 매칭 점수"""
        return result.get("industry_score", result.get("payload_score", 0.0))
    
    def _score_specialization_match(self, result: Dict) -> float:
        """전문분야 매칭 점수"""
        return result.get("specialization_score", result.get("payload_score", 0.0))
    
    def _score_experience_match(self, result: Dict) -> float:
        """경력 매칭 점수"""
        return result.get("experience_score", result.get("payload_score", 0.0))
    
    def _score_talent_level_match(self, result: Dict) -> float:
        """인재등급 매칭 점수"""
        return result.get("talent_level_score", result.get("payload_score", 0.0))
    
    def _score_skills_match(self, result: Dict) -> float:
        """기술스택 매칭 점수"""
        return result.get("skills_score", result.get("payload_score", 0.0))
    
    def apply_business_rules(self, results: List[Dict]) -> List[Dict]:
        """비즈니스 규칙 적용"""
        print("📊 비즈니스 규칙 적용")
        
        for result in results:
            # 1. 완전 매칭 보너스
            if self._is_perfect_match(result):
                result["final_score"] *= 1.2
                result["bonus_reasons"] = result.get("bonus_reasons", []) + ["완전 매칭"]
            
            # 2. 과도한 경력 페널티
            if self._is_overqualified(result):
                result["final_score"] *= 0.9
                result["penalty_reasons"] = result.get("penalty_reasons", []) + ["과도한 경력"]
            
            # 3. 지역 선호도 보너스
            if self._has_location_preference(result):
                result["final_score"] *= 1.1
                result["bonus_reasons"] = result.get("bonus_reasons", []) + ["지역 선호"]
            
            # 4. 긴급 요청 우선순위
            if self._is_urgent_request(result):
                result["final_score"] *= 1.15
                result["bonus_reasons"] = result.get("bonus_reasons", []) + ["긴급 요청"]
        
        # 규칙 적용 후 재정렬
        results.sort(key=lambda x: x["final_score"], reverse=True)
        
        return results
    
    def _is_perfect_match(self, result: Dict) -> bool:
        """완전 매칭 여부 확인"""
        payload_score = result.get("payload_score", 0.0)
        vector_score = result.get("vector_score", 0.0)
        
        return payload_score >= 0.9 and vector_score >= 0.85
    
    def _is_overqualified(self, result: Dict) -> bool:
        """과도한 경력 여부 확인"""
        experience = result.get("experience_years", 0)
        talent_level = result.get("talent_level", "")
        
        # 15년 이상 경력의 고급 인재가 중급 요구사항에 지원하는 경우
        return experience >= 15 and "중급" in str(talent_level)
    
    def _has_location_preference(self, result: Dict) -> bool:
        """지역 선호도 확인"""
        residence = result.get("residence", "")
        
        # 서울/경기 지역 선호도
        return residence in ["서울", "경기도"]
    
    def _is_urgent_request(self, result: Dict) -> bool:
        """긴급 요청 여부 확인"""
        # 쿼리나 결과에서 긴급 키워드 확인
        return "긴급" in str(result.get("requirement_type", []))
    
    def diversify_results(self, results: List[Dict], diversity_factor: float = 0.1) -> List[Dict]:
        """결과 다양성 증진"""
        print("🎯 결과 다양성 증진")
        
        if len(results) <= 1:
            return results
        
        diversified = [results[0]]  # 최고 점수는 유지
        
        for candidate in results[1:]:
            # 기존 선택된 후보들과의 다양성 계산
            diversity_score = self._calculate_diversity(candidate, diversified)
            
            # 다양성 보너스 적용
            candidate["final_score"] += diversity_score * diversity_factor
            candidate["diversity_score"] = diversity_score
        
        # 다양성이 적용된 점수로 재정렬
        results[1:] = sorted(results[1:], key=lambda x: x["final_score"], reverse=True)
        
        return results
    
    def _calculate_diversity(self, candidate: Dict, selected: List[Dict]) -> float:
        """다양성 점수 계산"""
        diversity_factors = ["specialization", "residence", "industry_domain", "talent_level"]
        
        diversity_score = 0.0
        
        for factor in diversity_factors:
            candidate_value = candidate.get(factor)
            
            # 선택된 후보들과 다른 값일 때 다양성 점수 증가
            different_count = sum(1 for s in selected if s.get(factor) != candidate_value)
            
            if different_count > 0:
                diversity_score += different_count / len(selected)
        
        return diversity_score / len(diversity_factors)
    
    def explain_ranking(self, result: Dict, weights: Dict) -> Dict:
        """순위 결정 이유 설명"""
        
        explanation = {
            "final_score": result.get("final_score", 0.0),
            "final_rank": result.get("final_rank", 0),
            "score_breakdown": {},
            "key_strengths": [],
            "improvement_areas": [],
            "bonuses_penalties": {}
        }
        
        # 점수 분해
        for field, weight in weights.items():
            if field != "vector_fields":
                field_score = self._calculate_field_score(result, field)
                weighted_score = field_score * weight
                
                explanation["score_breakdown"][field] = {
                    "raw_score": round(field_score, 3),
                    "weight": round(weight, 3),
                    "weighted_score": round(weighted_score, 3)
                }
        
        # 벡터 점수
        vector_score = result.get("vector_score", 0.0)
        explanation["score_breakdown"]["vector_fields"] = {
            "raw_score": round(vector_score, 3),
            "weight": 0.4,
            "weighted_score": round(vector_score * 0.4, 3)
        }
        
        # 주요 강점 식별
        explanation["key_strengths"] = self._identify_strengths(result, weights)
        
        # 개선 영역 식별
        explanation["improvement_areas"] = self._identify_weaknesses(result, weights)
        
        # 보너스/페널티
        explanation["bonuses_penalties"] = {
            "bonuses": result.get("bonus_reasons", []),
            "penalties": result.get("penalty_reasons", [])
        }
        
        return explanation
    
    def _identify_strengths(self, result: Dict, weights: Dict) -> List[str]:
        """주요 강점 식별"""
        strengths = []
        
        for field, weight in weights.items():
            if field != "vector_fields":
                field_score = self._calculate_field_score(result, field)
                if field_score >= 0.8:
                    strengths.append(f"{field}: 우수한 매칭 ({field_score:.2f})")
        
        return strengths
    
    def _identify_weaknesses(self, result: Dict, weights: Dict) -> List[str]:
        """개선 영역 식별"""
        weaknesses = []
        
        for field, weight in weights.items():
            if field != "vector_fields":
                field_score = self._calculate_field_score(result, field)
                if field_score <= 0.3 and weight > 0.15:  # 중요한 필드인데 점수 낮음
                    weaknesses.append(f"{field}: 매칭 부족 ({field_score:.2f})")
        
        return weaknesses