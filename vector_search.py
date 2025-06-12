"""
벡터 검색 모듈
벡터 필드를 기반으로 의미적 유사도 검색 수행
"""

import math
from typing import Dict, List, Optional, Tuple
import re
import logging

# 로깅 설정
logger = logging.getLogger(__name__)

class VectorSearcher:
    """벡터 기반 검색 클래스"""
    
    def __init__(self):
        # 벡터 필드 가중치
        self.vector_weights = {
            "professional_competency": 0.25,
            "technical_expertise": 0.30,
            "leadership_experience": 0.15,
            "scale_complexity": 0.10,
            "compliance_security": 0.15,
            "industry_specialization": 0.20
        }
        
        # 키워드 임베딩 시뮬레이션용 매핑
        self.keyword_vectors = self._init_keyword_vectors()
        
        print("🔍 벡터 검색기 초기화 완료")
    
    def _init_keyword_vectors(self) -> Dict:
        """키워드 벡터 매핑 초기화 (실제 환경에서는 임베딩 모델 사용)"""
        return {
            # 전문 역량 관련
            "유지보수": {"maintenance": 1.0, "operation": 0.8, "support": 0.7},
            "구축": {"construction": 1.0, "implementation": 0.9, "development": 0.8},
            "설계": {"design": 1.0, "architecture": 0.9, "planning": 0.7},
            "운영": {"operation": 1.0, "maintenance": 0.8, "monitoring": 0.7},
            "모니터링": {"monitoring": 1.0, "surveillance": 0.8, "tracking": 0.7},
            
            # 기술 전문성 관련
            "네트워크": {"network": 1.0, "infrastructure": 0.8, "connectivity": 0.7},
            "시스템": {"system": 1.0, "infrastructure": 0.8, "platform": 0.7},
            "데이터베이스": {"database": 1.0, "data": 0.8, "storage": 0.7},
            "보안": {"security": 1.0, "protection": 0.8, "safety": 0.7},
            "클라우드": {"cloud": 1.0, "aws": 0.9, "azure": 0.9},
            
            # 산업 전문성 관련
            "금융": {"finance": 1.0, "banking": 0.9, "investment": 0.8},
            "제조": {"manufacturing": 1.0, "production": 0.8, "factory": 0.7},
            "공공": {"public": 1.0, "government": 0.9, "administrative": 0.7},
            "에너지": {"energy": 1.0, "power": 0.9, "electric": 0.8},
            
            # 리더십 관련
            "팀장": {"team_lead": 1.0, "manager": 0.9, "supervisor": 0.8},
            "관리": {"management": 1.0, "administration": 0.8, "supervision": 0.7},
            "리더십": {"leadership": 1.0, "management": 0.8, "guidance": 0.7}
        }
    
    def search(self, parsed_query: Dict, payload_candidates: List[Dict]) -> List[Dict]:
        """벡터 검색 실행"""
        logger.info("🔍 벡터 검색 시작")
        
        if not payload_candidates:
            logger.warning("⚠️ Payload 후보가 없음")
            return []
        
        try:
            # 쿼리 벡터 생성
            query_vector = self._create_query_vector(parsed_query)
            
            results = []
            
            for candidate in payload_candidates:
                # 후보자 벡터 생성
                candidate_vector = self._create_candidate_vector(candidate)
                
                # 유사도 계산
                similarity_score = self._calculate_vector_similarity(query_vector, candidate_vector)
                
                # Payload 점수와 벡터 점수 결합
                payload_score = candidate.get("payload_score", 0.0)
                combined_score = self._combine_scores(payload_score, similarity_score)
                
                candidate_with_scores = candidate.copy()
                candidate_with_scores["vector_score"] = similarity_score
                candidate_with_scores["combined_score"] = combined_score
                
                results.append(candidate_with_scores)
            
            # 결합 점수로 정렬
            results.sort(key=lambda x: x.get("combined_score", 0), reverse=True)
            
            logger.info(f"✅ 벡터 검색 완료: {len(results)}명 결과")
            return results
            
        except Exception as e:
            logger.error(f"❌ 벡터 검색 오류: {e}")
            return payload_candidates
    
    def _create_query_vector(self, parsed_query: Dict) -> Dict:
        """쿼리에서 벡터 생성"""
        query_vector = {}
        
        try:
            vector_fields = parsed_query.get("vector_fields", {})
            
            for field, content in vector_fields.items():
                if content:
                    query_vector[field] = self._text_to_vector(content)
                else:
                    # 쿼리에서 추론 가능한 벡터 생성
                    query_vector[field] = self._infer_vector_from_query(field, parsed_query)
                    
        except Exception as e:
            logger.warning(f"쿼리 벡터 생성 오류: {e}")
        
        return query_vector
    
    def _create_candidate_vector(self, candidate: Dict) -> Dict:
        """후보자에서 벡터 생성"""
        candidate_vector = {}
        
        try:
            # 후보자의 벡터 필드 직접 사용
            vector_fields = candidate.get("vector_fields", {})
            
            for field in self.vector_weights.keys():
                content = vector_fields.get(field)
                if content:
                    candidate_vector[field] = self._text_to_vector(content)
                else:
                    # 후보자 정보에서 벡터 추론
                    candidate_vector[field] = self._infer_vector_from_candidate(field, candidate)
                    
        except Exception as e:
            logger.warning(f"후보자 벡터 생성 오류: {e}")
        
        return candidate_vector
    
    def _text_to_vector(self, text: str) -> Dict:
        """텍스트를 벡터로 변환 (키워드 기반 시뮬레이션)"""
        if not text:
            return {}
        
        try:
            text_lower = text.lower()
            vector = {}
            
            # 키워드 매칭으로 벡터 생성
            for keyword, keyword_vector in self.keyword_vectors.items():
                if keyword in text_lower:
                    for vec_key, vec_value in keyword_vector.items():
                        vector[vec_key] = vector.get(vec_key, 0) + vec_value
            
            # 정규화
            if vector:
                total = sum(vector.values())
                if total > 0:
                    vector = {k: v/total for k, v in vector.items()}
            
            return vector
            
        except Exception as e:
            logger.warning(f"텍스트 벡터 변환 오류: {e}")
            return {}
    
    def _infer_vector_from_query(self, field: str, parsed_query: Dict) -> Dict:
        """쿼리에서 벡터 필드 추론"""
        vector = {}
        
        try:
            if field == "professional_competency":
                # 전문 역량 추론
                specialization = parsed_query.get("specialization")
                if specialization == "NE":
                    vector = {"network": 0.8, "infrastructure": 0.6, "maintenance": 0.4}
                elif specialization == "DBA":
                    vector = {"database": 0.9, "data": 0.7, "maintenance": 0.5}
                elif specialization == "보안":
                    vector = {"security": 0.9, "protection": 0.7, "monitoring": 0.5}
                elif specialization == "OP":
                    vector = {"operation": 0.9, "maintenance": 0.8, "monitoring": 0.6}
            
            elif field == "technical_expertise":
                # 기술 전문성 추론
                skills = parsed_query.get("skills", [])
                for skill in skills:
                    skill_lower = skill.lower()
                    if "network" in skill_lower or "cisco" in skill_lower:
                        vector["network"] = vector.get("network", 0) + 0.3
                    elif "database" in skill_lower or "oracle" in skill_lower:
                        vector["database"] = vector.get("database", 0) + 0.3
                    elif "cloud" in skill_lower or "aws" in skill_lower:
                        vector["cloud"] = vector.get("cloud", 0) + 0.3
            
            elif field == "industry_specialization":
                # 산업 전문성 추론
                industry = parsed_query.get("industry_domain")
                if industry == "금융":
                    vector = {"finance": 0.8, "banking": 0.6}
                elif industry == "제조":
                    vector = {"manufacturing": 0.8, "production": 0.6}
                elif industry == "공공":
                    vector = {"public": 0.8, "government": 0.6}
                elif industry == "에너지":
                    vector = {"energy": 0.8, "power": 0.6}
            
            elif field == "leadership_experience":
                # 리더십 경험 추론
                experience = parsed_query.get("experience_years", 0)
                talent_level = parsed_query.get("talent_level", [])
                if experience >= 7 or "고급" in talent_level:
                    vector = {"leadership": 0.7, "management": 0.5}
                elif experience >= 5:
                    vector = {"team_lead": 0.6, "guidance": 0.4}
            
            elif field == "scale_complexity":
                # 규모/복잡성 추론
                if parsed_query.get("industry_domain") in ["금융", "공공"]:
                    vector = {"enterprise": 0.7, "complex": 0.5}
            
            elif field == "compliance_security":
                # 컴플라이언스/보안 추론
                if parsed_query.get("industry_domain") in ["금융", "공공"]:
                    vector = {"security": 0.8, "compliance": 0.6}
                elif parsed_query.get("specialization") == "보안":
                    vector = {"security": 0.9, "protection": 0.7}
                    
        except Exception as e:
            logger.warning(f"쿼리 벡터 추론 오류 ({field}): {e}")
        
        return vector
    
    def _infer_vector_from_candidate(self, field: str, candidate: Dict) -> Dict:
        """후보자 정보에서 벡터 필드 추론"""
        vector = {}
        
        try:
            if field == "technical_expertise":
                # 기술 전문성 추론
                spec = candidate.get("specialization")
                skills = candidate.get("skills", [])
                
                if spec == "NE":
                    vector = {"network": 0.8, "infrastructure": 0.6}
                elif spec == "DBA":
                    vector = {"database": 0.9, "data": 0.7}
                elif spec == "보안":
                    vector = {"security": 0.9, "protection": 0.7}
                elif spec == "SE":
                    vector = {"system": 0.8, "infrastructure": 0.6}
                elif spec == "DVLP":
                    vector = {"development": 0.8, "programming": 0.6}
                elif spec == "OP":
                    vector = {"operation": 0.9, "maintenance": 0.7}
                
                # 스킬에서 추가 벡터 추론
                for skill in skills:
                    skill_lower = skill.lower()
                    if "aws" in skill_lower or "cloud" in skill_lower:
                        vector["cloud"] = vector.get("cloud", 0) + 0.3
            
            elif field == "industry_specialization":
                # 산업 전문성 추론
                industry = candidate.get("industry_domain")
                knowledge = candidate.get("industry_knowledge")
                
                if industry == "금융":
                    vector["finance"] = 0.8
                    if knowledge == "은행":
                        vector["banking"] = 0.9
                    elif knowledge == "보험":
                        vector["insurance"] = 0.9
                elif industry == "에너지":
                    vector["energy"] = 0.8
                    vector["power"] = 0.6
                elif industry == "제조":
                    vector["manufacturing"] = 0.8
                    vector["production"] = 0.6
                elif industry == "공공":
                    vector["public"] = 0.8
                    vector["government"] = 0.6
            
            elif field == "leadership_experience":
                # 리더십 경험 추론
                experience = candidate.get("experience_years", 0)
                level = candidate.get("talent_level")
                
                if level == "고급" and experience >= 8:
                    vector = {"leadership": 0.8, "management": 0.6}
                elif experience >= 5:
                    vector = {"team_lead": 0.6}
            
            elif field == "professional_competency":
                # 전문 역량 추론
                spec = candidate.get("specialization")
                if spec == "NE":
                    vector = {"network": 0.7, "maintenance": 0.5}
                elif spec == "SE":
                    vector = {"system": 0.7, "operation": 0.6}
                elif spec == "OP":
                    vector = {"operation": 0.8, "maintenance": 0.7}
                elif spec == "DVLP":
                    vector = {"development": 0.8, "programming": 0.6}
            
            elif field == "scale_complexity":
                # 규모/복잡성 추론
                experience = candidate.get("experience_years", 0)
                industry = candidate.get("industry_domain")
                if experience >= 7 and industry in ["금융", "공공"]:
                    vector = {"enterprise": 0.6, "complex": 0.4}
            
            elif field == "compliance_security":
                # 컴플라이언스/보안 추론
                spec = candidate.get("specialization")
                industry = candidate.get("industry_domain")
                if spec == "보안":
                    vector = {"security": 0.9, "protection": 0.7}
                elif industry in ["금융", "공공"]:
                    vector = {"security": 0.5, "compliance": 0.4}
                    
        except Exception as e:
            logger.warning(f"후보자 벡터 추론 오류 ({field}): {e}")
        
        return vector
    
    def _calculate_vector_similarity(self, query_vector: Dict, candidate_vector: Dict) -> float:
        """벡터 간 유사도 계산"""
        try:
            total_similarity = 0.0
            
            for field, weight in self.vector_weights.items():
                query_field_vector = query_vector.get(field, {})
                candidate_field_vector = candidate_vector.get(field, {})
                
                if not query_field_vector and not candidate_field_vector:
                    field_similarity = 0.5  # 둘 다 없으면 중립
                elif not query_field_vector or not candidate_field_vector:
                    field_similarity = 0.0  # 한쪽만 없으면 0
                else:
                    field_similarity = self._cosine_similarity(query_field_vector, candidate_field_vector)
                
                total_similarity += field_similarity * weight
            
            return total_similarity
            
        except Exception as e:
            logger.warning(f"벡터 유사도 계산 오류: {e}")
            return 0.0
    
    def _cosine_similarity(self, vector1: Dict, vector2: Dict) -> float:
        """코사인 유사도 계산"""
        try:
            # 공통 키 찾기
            common_keys = set(vector1.keys()) & set(vector2.keys())
            
            if not common_keys:
                return 0.0
            
            # 내적 계산
            dot_product = sum(vector1[key] * vector2[key] for key in common_keys)
            
            # 크기 계산
            magnitude1 = math.sqrt(sum(v*v for v in vector1.values()))
            magnitude2 = math.sqrt(sum(v*v for v in vector2.values()))
            
            if magnitude1 == 0 or magnitude2 == 0:
                return 0.0
            
            return dot_product / (magnitude1 * magnitude2)
            
        except Exception as e:
            logger.warning(f"코사인 유사도 계산 오류: {e}")
            return 0.0
    
    def _combine_scores(self, payload_score: float, vector_score: float) -> float:
        """Payload 점수와 벡터 점수 결합"""
        try:
            # 가중 평균 (Payload 60%, Vector 40%)
            payload_weight = 0.6
            vector_weight = 0.4
            
            combined = payload_score * payload_weight + vector_score * vector_weight
            return max(0.0, min(1.0, combined))  # 0-1 범위로 제한
            
        except Exception as e:
            logger.warning(f"점수 결합 오류: {e}")
            return payload_score  # 오류 시 payload 점수만 반환
    
    def explain_vector_matching(self, query_vector: Dict, candidate_vector: Dict) -> Dict:
        """벡터 매칭 결과 설명"""
        explanations = {}
        
        try:
            for field, weight in self.vector_weights.items():
                query_field = query_vector.get(field, {})
                candidate_field = candidate_vector.get(field, {})
                
                if query_field and candidate_field:
                    similarity = self._cosine_similarity(query_field, candidate_field)
                    
                    # 매칭된 키워드 찾기
                    common_keywords = set(query_field.keys()) & set(candidate_field.keys())
                    
                    explanations[field] = {
                        "similarity": round(similarity, 3),
                        "weight": weight,
                        "weighted_score": round(similarity * weight, 3),
                        "matched_concepts": list(common_keywords),
                        "explanation": self._get_field_explanation(field, similarity)
                    }
                    
        except Exception as e:
            logger.warning(f"벡터 매칭 설명 오류: {e}")
        
        return explanations
    
    def _get_field_explanation(self, field: str, similarity: float) -> str:
        """필드별 매칭 설명"""
        explanations = {
            "professional_competency": "실무 역량 매칭도",
            "technical_expertise": "기술 전문성 유사도",
            "leadership_experience": "리더십 경험 적합도",
            "scale_complexity": "프로젝트 규모 경험",
            "compliance_security": "보안/컴플라이언스 경험",
            "industry_specialization": "산업 전문성 매칭도"
        }
        
        base_explanation = explanations.get(field, "매칭도")
        
        if similarity >= 0.8:
            return f"{base_explanation}: 매우 높음"
        elif similarity >= 0.6:
            return f"{base_explanation}: 높음"
        elif similarity >= 0.4:
            return f"{base_explanation}: 보통"
        elif similarity >= 0.2:
            return f"{base_explanation}: 낮음"
        else:
            return f"{base_explanation}: 매우 낮음"
    
    def get_top_matches_by_vector_field(self, results: List[Dict], field: str, limit: int = 5) -> List[Dict]:
        """특정 벡터 필드 기준 상위 매칭 결과"""
        try:
            # 해당 필드의 벡터 점수 계산
            scored_results = []
            
            for result in results:
                candidate_vector = self._create_candidate_vector(result)
                field_vector = candidate_vector.get(field, {})
                
                if field_vector:
                    # 필드별 점수 계산 (간단히 벡터 크기로)
                    field_score = sum(field_vector.values())
                    
                    result_copy = result.copy()
                    result_copy[f"{field}_score"] = field_score
                    scored_results.append(result_copy)
            
            # 필드 점수로 정렬
            scored_results.sort(key=lambda x: x.get(f"{field}_score", 0), reverse=True)
            
            return scored_results[:limit]
            
        except Exception as e:
            logger.warning(f"필드별 상위 매칭 결과 오류: {e}")
            return results[:limit]