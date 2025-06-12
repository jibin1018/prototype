"""
챗봇 형식 추천 이유 생성기
매칭률에 따른 지능적 추천 및 대화형 응답 생성
"""

from typing import Dict, List, Optional
import random
import logging

# 로깅 설정
logger = logging.getLogger(__name__)

class ChatbotRecommendationGenerator:
    """챗봇 형식 추천 이유 생성 클래스"""
    
    def __init__(self):
        # 매칭률 기준 설정
        self.matching_thresholds = {
            "excellent": 85,    # 85% 이상 - 강력 추천
            "good": 70,         # 70% 이상 - 추천
            "fair": 55,         # 55% 이상 - 조건부 추천
            "poor": 40          # 40% 이상 - 추천 안함 (대안 제시)
        }
        
        # 챗봇 응답 템플릿
        self.chatbot_templates = self._init_chatbot_templates()
        self.conversation_starters = self._init_conversation_starters()
        self.alternative_suggestions = self._init_alternative_suggestions()
        
        print("🤖 챗봇 형식 추천 시스템 초기화 완료")
    
    def _init_chatbot_templates(self) -> Dict:
        """챗봇 응답 템플릿 초기화"""
        return {
            "excellent_intro": [
                "🎉 훌륭한 소식이 있어요! 요청하신 조건에 완벽하게 맞는 최고의 인재들을 찾았습니다.",
                "😊 정말 좋은 결과가 나왔어요! 요구사항과 거의 완벽하게 일치하는 우수한 후보자들이 있습니다.",
                "✨ 기대 이상의 결과입니다! 모든 조건을 만족하는 뛰어난 전문가들을 발견했어요."
            ],
            "good_intro": [
                "👍 좋은 소식이에요! 요청하신 조건에 잘 맞는 우수한 인재들을 찾았습니다.",
                "😄 만족할 만한 결과가 나왔어요! 대부분의 조건을 충족하는 좋은 후보자들이 있습니다.",
                "🌟 괜찮은 매칭 결과예요! 핵심 조건들을 잘 만족하는 인재들을 추천드릴 수 있어요."
            ],
            "fair_intro": [
                "🤔 몇 가지 옵션이 있긴 하지만, 완전히 만족스럽지는 않을 수 있어요.",
                "😐 기본 조건은 만족하지만 일부 요구사항에서 타협이 필요한 후보자들이 있습니다.",
                "💭 조건부로 고려해볼 만한 인재들은 있어요. 하지만 추가 검토가 필요할 것 같아요."
            ],
            "poor_intro": [
                "😔 아쉽게도 요청하신 조건에 정확히 맞는 인재를 찾기가 어려웠어요.",
                "🤷‍♀️ 현재 데이터베이스에서는 완전히 적합한 후보를 찾지 못했습니다.",
                "😞 원하시는 조건의 인재가 부족한 상황이에요."
            ],
            "no_results": [
                "🔍 검색 조건을 다시 확인해보시겠어요? 현재 조건으로는 매칭되는 인재가 없어요.",
                "💡 조건을 조금 완화하시면 더 많은 후보를 찾을 수 있을 것 같아요.",
                "🎯 다른 접근 방법을 제안드릴 수 있어요. 어떤 조건이 가장 중요하신지 말씀해 주세요."
            ]
        }
    
    def _init_conversation_starters(self) -> Dict:
        """대화 시작 문구 초기화"""
        return {
            "greeting": [
                "안녕하세요! 인재 검색을 도와드릴게요. 어떤 분을 찾고 계신가요?",
                "반갑습니다! 원하시는 인재의 조건을 말씀해 주시면 최적의 후보를 찾아드려요.",
                "안녕하세요! 어떤 전문성을 가진 인재를 찾고 계신지 알려주세요."
            ],
            "analysis_start": [
                "네, 알겠습니다! 지금 데이터베이스를 분석해보고 있어요...",
                "조건을 확인했어요. 최적의 인재를 찾기 위해 검색 중입니다...",
                "말씀해 주신 조건으로 인재풀을 분석하고 있습니다. 잠시만 기다려 주세요..."
            ]
        }
    
    def _init_alternative_suggestions(self) -> Dict:
        """대안 제안 초기화"""
        return {
            "relaxation_suggestions": [
                "💡 경력 조건을 조금 완화해보시는 건 어떨까요?",
                "🔄 지역 범위를 넓혀서 다시 검색해보는 것을 추천드려요.",
                "⚡ 필수 기술 스택을 줄이고 우대 조건으로 변경해보시겠어요?",
                "📈 인재 등급을 '등급무관'으로 설정하면 더 많은 후보를 찾을 수 있어요."
            ],
            "alternative_approaches": [
                "🎯 다른 전문 분야의 인재 중에서 적응 가능한 분들을 찾아볼까요?",
                "🌐 원격 근무가 가능하다면 지역 제한 없이 검색할 수 있어요.",
                "⏰ 시급하지 않으시다면 조건에 맞는 신규 인재 등록을 기다려보는 것도 방법이에요.",
                "📊 시장 현황을 보면 해당 조건의 인재는 희소합니다. 조건 조정을 권장해요."
            ]
        }
    
    def generate_chatbot_response(self, user_query: str, parsed_query: Dict, 
                                ranked_talents: List[Dict]) -> Dict:
        """챗봇 형식 응답 생성 메인 함수"""
        logger.info("🤖 챗봇 응답 생성 시작")
        
        try:
            # 매칭률 분석
            matching_analysis = self._analyze_matching_quality(ranked_talents)
            
            # 응답 타입 결정
            response_type = self._determine_response_type(matching_analysis)
            
            # 챗봇 응답 생성
            chatbot_response = self._generate_response_by_type(
                response_type, user_query, parsed_query, ranked_talents, matching_analysis
            )
            
            logger.info(f"✅ 챗봇 응답 생성 완료: {response_type} 타입")
            return chatbot_response
            
        except Exception as e:
            logger.error(f"❌ 챗봇 응답 생성 오류: {e}")
            return self._generate_error_response()
    
    def _analyze_matching_quality(self, ranked_talents: List[Dict]) -> Dict:
        """매칭 품질 분석"""
        try:
            if not ranked_talents:
                return {
                    "average_score": 0,
                    "top_score": 0,
                    "candidate_count": 0,
                    "quality_level": "none"
                }
            
            # 점수 추출 및 계산
            scores = []
            for talent in ranked_talents:
                score = talent.get("final_score", talent.get("combined_score", 0.0)) * 100
                scores.append(score)
            
            analysis = {
                "average_score": sum(scores) / len(scores) if scores else 0,
                "top_score": max(scores) if scores else 0,
                "candidate_count": len(ranked_talents),
                "score_distribution": scores,
                "quality_level": self._determine_quality_level(max(scores) if scores else 0)
            }
            
            return analysis
            
        except Exception as e:
            logger.warning(f"매칭 품질 분석 오류: {e}")
            return {"average_score": 0, "top_score": 0, "candidate_count": 0, "quality_level": "none"}
    
    def _determine_quality_level(self, top_score: float) -> str:
        """품질 수준 결정"""
        if top_score >= self.matching_thresholds["excellent"]:
            return "excellent"
        elif top_score >= self.matching_thresholds["good"]:
            return "good"
        elif top_score >= self.matching_thresholds["fair"]:
            return "fair"
        elif top_score >= self.matching_thresholds["poor"]:
            return "poor"
        else:
            return "none"
    
    def _determine_response_type(self, matching_analysis: Dict) -> str:
        """응답 타입 결정"""
        quality_level = matching_analysis.get("quality_level", "none")
        candidate_count = matching_analysis.get("candidate_count", 0)
        
        if candidate_count == 0:
            return "no_results"
        elif quality_level in ["excellent", "good"]:
            return "recommend"
        elif quality_level == "fair":
            return "conditional_recommend"
        else:
            return "suggest_alternatives"
    
    def _generate_response_by_type(self, response_type: str, user_query: str, 
                                 parsed_query: Dict, ranked_talents: List[Dict], 
                                 matching_analysis: Dict) -> Dict:
        """타입별 응답 생성"""
        
        if response_type == "no_results":
            return self._generate_no_results_response(user_query, parsed_query)
        
        elif response_type == "recommend":
            return self._generate_recommendation_response(
                user_query, parsed_query, ranked_talents, matching_analysis
            )
        
        elif response_type == "conditional_recommend":
            return self._generate_conditional_response(
                user_query, parsed_query, ranked_talents, matching_analysis
            )
        
        elif response_type == "suggest_alternatives":
            return self._generate_alternative_response(
                user_query, parsed_query, ranked_talents, matching_analysis
            )
        
        else:
            return self._generate_error_response()
    
    def _generate_recommendation_response(self, user_query: str, parsed_query: Dict, 
                                        ranked_talents: List[Dict], matching_analysis: Dict) -> Dict:
        """추천 응답 생성"""
        try:
            quality_level = matching_analysis.get("quality_level", "good")
            top_score = matching_analysis.get("top_score", 0)
            
            # 인사말 선택
            if quality_level == "excellent":
                intro = random.choice(self.chatbot_templates["excellent_intro"])
            else:
                intro = random.choice(self.chatbot_templates["good_intro"])
            
            # 상위 3명 또는 최고 매칭만 선별
            recommended_talents = self._select_recommended_talents(ranked_talents, matching_analysis)
            
            # 상세 정보 생성
            detailed_recommendations = []
            for i, talent in enumerate(recommended_talents):
                detailed_rec = self._generate_detailed_recommendation(
                    user_query, parsed_query, talent, i + 1
                )
                detailed_recommendations.append(detailed_rec)
            
            # 챗봇 메시지 생성
            summary_message = self._generate_summary_message(recommended_talents, matching_analysis)
            
            return {
                "response_type": "recommend",
                "message": intro,
                "summary": summary_message,
                "recommendations": detailed_recommendations,
                "matching_analysis": matching_analysis,
                "chatbot_tone": "positive",
                "next_actions": [
                    "상위 후보자와 면접 일정을 잡아보세요",
                    "더 자세한 정보가 필요하시면 말씀해 주세요",
                    "다른 조건으로 추가 검색도 가능해요"
                ]
            }
            
        except Exception as e:
            logger.warning(f"추천 응답 생성 오류: {e}")
            return self._generate_error_response()
    
    def _generate_conditional_response(self, user_query: str, parsed_query: Dict, 
                                     ranked_talents: List[Dict], matching_analysis: Dict) -> Dict:
        """조건부 추천 응답 생성"""
        try:
            intro = random.choice(self.chatbot_templates["fair_intro"])
            
            # 최고 점수 후보 1-2명만 선별
            top_candidates = ranked_talents[:2] if len(ranked_talents) >= 2 else ranked_talents
            
            detailed_recommendations = []
            for i, talent in enumerate(top_candidates):
                detailed_rec = self._generate_detailed_recommendation(
                    user_query, parsed_query, talent, i + 1
                )
                # 조건부 추천 특별 메모 추가
                detailed_rec["conditional_note"] = self._generate_conditional_note(talent, parsed_query)
                detailed_recommendations.append(detailed_rec)
            
            return {
                "response_type": "conditional_recommend",
                "message": intro,
                "summary": f"조건을 부분적으로 만족하는 {len(detailed_recommendations)}명의 후보가 있어요. 추가 검토를 권장드려요.",
                "recommendations": detailed_recommendations,
                "matching_analysis": matching_analysis,
                "chatbot_tone": "cautious",
                "considerations": [
                    "일부 조건에서 타협이 필요할 수 있어요",
                    "추가 면접을 통한 검증을 권장해요",
                    "조건을 조정하면 더 나은 후보를 찾을 수도 있어요"
                ],
                "next_actions": [
                    "조건을 완화해서 재검색해보세요",
                    "현재 후보들과 면접을 진행해보세요",
                    "어떤 조건이 가장 중요한지 알려주세요"
                ]
            }
            
        except Exception as e:
            logger.warning(f"조건부 추천 응답 생성 오류: {e}")
            return self._generate_error_response()
    
    def _generate_alternative_response(self, user_query: str, parsed_query: Dict, 
                                     ranked_talents: List[Dict], matching_analysis: Dict) -> Dict:
        """대안 제안 응답 생성"""
        try:
            intro = random.choice(self.chatbot_templates["poor_intro"])
            
            # 현재 최고 점수 후보가 있다면 1명만 참고용으로 제시
            reference_candidate = None
            if ranked_talents:
                best_candidate = ranked_talents[0]
                score = best_candidate.get("final_score", best_candidate.get("combined_score", 0.0)) * 100
                if score >= self.matching_thresholds["poor"]:
                    reference_candidate = self._generate_detailed_recommendation(
                        user_query, parsed_query, best_candidate, 1
                    )
                    reference_candidate["is_reference"] = True
            
            # 구체적인 대안 제안 생성
            suggestions = self._generate_specific_suggestions(parsed_query, matching_analysis)
            
            return {
                "response_type": "suggest_alternatives",
                "message": intro,
                "summary": "더 나은 결과를 위해 몇 가지 제안을 드릴게요.",
                "reference_candidate": reference_candidate,
                "matching_analysis": matching_analysis,
                "chatbot_tone": "helpful",
                "suggestions": suggestions,
                "next_actions": [
                    "제안된 조건 완화를 고려해보세요",
                    "시장 현황을 확인해보시겠어요?",
                    "다른 접근 방법을 시도해보세요"
                ]
            }
            
        except Exception as e:
            logger.warning(f"대안 제안 응답 생성 오류: {e}")
            return self._generate_error_response()
    
    def _generate_no_results_response(self, user_query: str, parsed_query: Dict) -> Dict:
        """결과 없음 응답 생성"""
        try:
            intro = random.choice(self.chatbot_templates["no_results"])
            
            # 검색 조건 분석
            search_analysis = self._analyze_search_conditions(parsed_query)
            
            # 구체적인 완화 제안
            relaxation_suggestions = self._generate_relaxation_suggestions(parsed_query)
            
            return {
                "response_type": "no_results",
                "message": intro,
                "summary": "검색 조건을 조정해보시면 적합한 인재를 찾을 수 있을 거예요.",
                "search_analysis": search_analysis,
                "chatbot_tone": "encouraging",
                "suggestions": relaxation_suggestions,
                "next_actions": [
                    "검색 조건을 완화해보세요",
                    "다른 키워드로 검색해보세요",
                    "도움이 필요하시면 언제든 말씀해 주세요"
                ]
            }
            
        except Exception as e:
            logger.warning(f"결과 없음 응답 생성 오류: {e}")
            return self._generate_error_response()
    
    def _select_recommended_talents(self, ranked_talents: List[Dict], matching_analysis: Dict) -> List[Dict]:
        """추천할 인재 선별"""
        try:
            quality_level = matching_analysis.get("quality_level", "good")
            top_score = matching_analysis.get("top_score", 0)
            
            if quality_level == "excellent":
                # 85% 이상이면 상위 3명
                return ranked_talents[:3]
            elif quality_level == "good":
                # 70% 이상이면 상위 2-3명
                return ranked_talents[:3] if len(ranked_talents) >= 3 else ranked_talents
            else:
                # 그 외는 최고 점수자만
                return ranked_talents[:1] if ranked_talents else []
                
        except Exception as e:
            logger.warning(f"인재 선별 오류: {e}")
            return ranked_talents[:3] if ranked_talents else []
    
    def _generate_detailed_recommendation(self, user_query: str, parsed_query: Dict, 
                                        talent: Dict, rank: int) -> Dict:
        """상세 추천 정보 생성 (기존 함수 재사용)"""
        # 기존의 상세 추천 로직 재사용
        try:
            match_score = talent.get("final_score", talent.get("combined_score", 0.0)) * 100
            
            return {
                "id": talent.get("id", f"talent_{rank}"),
                "name": talent.get("name", f"인재 {rank}"),
                "rank": rank,
                "age": talent.get("age"),
                "residence": talent.get("residence"),
                "specialization": talent.get("specialization"),
                "experience": f"{talent.get('experience_years', 0)}년",
                "talent_level": talent.get("talent_level", "중급"),
                "industry_domain": talent.get("industry_domain"),
                "skills": talent.get("skills", [])[:6] if talent.get("skills") else [],
                "score": round(match_score, 1),
                "recommendation": self._generate_chatbot_style_recommendation(talent, match_score),
                "strengths": self._identify_key_strengths(talent)[:4],
                "considerations": self._generate_considerations(talent)[:3]
            }
            
        except Exception as e:
            logger.warning(f"상세 추천 생성 오류: {e}")
            return self._create_fallback_recommendation(talent, rank)
    
    def _generate_chatbot_style_recommendation(self, talent: Dict, match_score: float) -> str:
        """챗봇 스타일 추천 텍스트"""
        try:
            name = talent.get("name", "이 분")
            specialization = talent.get("specialization", "해당 분야")
            experience = talent.get("experience_years", 0)
            
            if match_score >= 90:
                return f"🌟 {name}님은 정말 완벽한 매칭이에요! {specialization} 분야에서 {experience}년 경력을 가지고 계시고, 요청하신 모든 조건을 만족합니다. 적극 추천드려요!"
            elif match_score >= 80:
                return f"👍 {name}님은 아주 좋은 후보예요! {specialization} 전문가로 {experience}년의 경력을 보유하고 계시며, 핵심 조건들을 잘 충족합니다."
            elif match_score >= 70:
                return f"😊 {name}님은 괜찮은 선택이 될 것 같아요. {specialization} 분야 {experience}년 경력으로 기본 요구사항을 만족하시지만, 일부 조건에서 검토가 필요해요."
            else:
                return f"🤔 {name}님은 부분적으로 조건에 맞아요. {experience}년의 경력을 가지고 계시지만, 몇 가지 요구사항에서 타협이 필요할 수 있어요."
                
        except Exception as e:
            logger.warning(f"챗봇 스타일 추천 텍스트 생성 오류: {e}")
            return "해당 분야의 경험을 가진 인재입니다."
    
    def _generate_conditional_note(self, talent: Dict, parsed_query: Dict) -> str:
        """조건부 추천 특별 메모"""
        try:
            issues = []
            
            # 경력 부족 체크
            talent_exp = talent.get("experience_years", 0)
            query_exp = parsed_query.get("experience_years", 0)
            if query_exp and talent_exp < query_exp:
                issues.append(f"요구 경력({query_exp}년) 대비 부족({talent_exp}년)")
            
            # 지역 불일치 체크
            if (talent.get("residence") != parsed_query.get("residence") and 
                parsed_query.get("residence")):
                issues.append("거주 지역 불일치")
            
            # 기술 스택 부족 체크
            talent_skills = talent.get("skills", [])
            query_skills = parsed_query.get("skills", [])
            if query_skills:
                matched = len([s for s in talent_skills if any(qs.lower() in s.lower() for qs in query_skills)])
                if matched < len(query_skills) * 0.7:
                    issues.append("일부 기술 스택 미보유")
            
            if issues:
                return f"⚠️ 고려사항: {', '.join(issues)}"
            else:
                return "✅ 기본 조건 충족, 추가 검토 권장"
                
        except Exception as e:
            logger.warning(f"조건부 메모 생성 오류: {e}")
            return "추가 검토가 필요한 후보입니다."
    
    def _generate_specific_suggestions(self, parsed_query: Dict, matching_analysis: Dict) -> List[str]:
        """구체적인 제안 생성"""
        try:
            suggestions = []
            
            # 경력 조건 완화
            if parsed_query.get("experience_years", 0) >= 5:
                suggestions.append(f"💡 경력 조건을 {parsed_query['experience_years']-2}년 이상으로 낮춰보세요")
            
            # 지역 확대
            if parsed_query.get("residence"):
                suggestions.append(f"🌐 {parsed_query['residence']} 외에 인근 지역도 포함해보세요")
            
            # 기술 스택 완화
            if parsed_query.get("skills") and len(parsed_query["skills"]) > 2:
                suggestions.append("⚡ 필수 기술을 핵심 2-3개로 줄여보세요")
            
            # 전문분야 확대
            if parsed_query.get("specialization"):
                suggestions.append("🔄 유사한 전문분야도 고려해보세요")
            
            # 기본 제안
            if not suggestions:
                suggestions.extend(random.sample(self.alternative_suggestions["relaxation_suggestions"], 2))
            
            return suggestions[:4]
            
        except Exception as e:
            logger.warning(f"구체적 제안 생성 오류: {e}")
            return ["조건을 조금 완화해보시는 것을 권장드려요."]
    
    def _generate_relaxation_suggestions(self, parsed_query: Dict) -> List[str]:
        """완화 제안 생성"""
        try:
            suggestions = []
            
            conditions = []
            if parsed_query.get("age_min") or parsed_query.get("age_max"):
                conditions.append("나이 조건")
            if parsed_query.get("residence"):
                conditions.append("지역 조건")
            if parsed_query.get("experience_years"):
                conditions.append("경력 조건")
            if parsed_query.get("skills"):
                conditions.append("기술 스택")
            if parsed_query.get("specialization"):
                conditions.append("전문분야")
            
            if conditions:
                suggestions.append(f"📝 현재 설정된 조건: {', '.join(conditions)}")
                suggestions.append(f"🎯 이 중에서 가장 중요한 조건 2-3개만 선택해보세요")
            
            suggestions.extend([
                "💼 '등급무관'으로 인재 등급을 확대해보세요",
                "🔍 유사한 키워드로 다시 검색해보세요"
            ])
            
            return suggestions
            
        except Exception as e:
            logger.warning(f"완화 제안 생성 오류: {e}")
            return ["검색 조건을 조금 완화해보시면 좋을 것 같아요."]
    
    def _analyze_search_conditions(self, parsed_query: Dict) -> Dict:
        """검색 조건 분석"""
        try:
            analysis = {
                "total_conditions": 0,
                "strict_conditions": [],
                "flexible_conditions": []
            }
            
            conditions = [
                ("나이", parsed_query.get("age") or parsed_query.get("age_min") or parsed_query.get("age_max")),
                ("거주지", parsed_query.get("residence")),
                ("경력", parsed_query.get("experience_years")),
                ("전문분야", parsed_query.get("specialization")),
                ("산업분야", parsed_query.get("industry_domain")),
                ("기술스택", parsed_query.get("skills")),
                ("인재등급", parsed_query.get("talent_level"))
            ]
            
            for name, value in conditions:
                if value:
                    analysis["total_conditions"] += 1
                    if name in ["경력", "기술스택"]:
                        analysis["strict_conditions"].append(name)
                    else:
                        analysis["flexible_conditions"].append(name)
            
            return analysis
            
        except Exception as e:
            logger.warning(f"검색 조건 분석 오류: {e}")
            return {"total_conditions": 0, "strict_conditions": [], "flexible_conditions": []}
    
    def _identify_key_strengths(self, talent: Dict) -> List[str]:
        """핵심 강점 식별 (간소화 버전)"""
        try:
            strengths = []
            
            # 경력 기반 강점
            experience = talent.get("experience_years", 0)
            if experience >= 10:
                strengths.append("풍부한 경험")
            elif experience >= 5:
                strengths.append("검증된 실무 능력")
            
            # 전문 분야 강점
            specialization = talent.get("specialization")
            if specialization:
                strengths.append(f"{specialization} 전문성")
            
            # 산업 경험
            industry = talent.get("industry_domain")
            if industry in ["금융", "공공"]:
                strengths.append("고도화된 업계 경험")
            
            # 기술 스택
            skills = talent.get("skills", [])
            if len(skills) >= 4:
                strengths.append("다양한 기술 보유")
            
            return strengths[:4]
            
        except Exception as e:
            logger.warning(f"강점 식별 오류: {e}")
            return ["전문성"]
    
    def _generate_considerations(self, talent: Dict) -> List[str]:
        """고려사항 생성 (간소화 버전)"""
        try:
            considerations = []
            
            # 경력 관련
            experience = talent.get("experience_years", 0)
            if experience >= 15:
                considerations.append("시니어급 연봉 수준")
            elif experience <= 2:
                considerations.append("교육 및 멘토링 필요")
            
            # 지역 관련
            residence = talent.get("residence")
            if residence not in ["서울", "경기도"]:
                considerations.append("원거리 거주")
            
            return considerations[:3]
            
        except Exception as e:
            logger.warning(f"고려사항 생성 오류: {e}")
            return []
    
    def _generate_summary_message(self, recommended_talents: List[Dict], matching_analysis: Dict) -> str:
        """요약 메시지 생성"""
        try:
            count = len(recommended_talents)
            avg_score = matching_analysis.get("average_score", 0)
            quality_level = matching_analysis.get("quality_level", "good")
            
            if quality_level == "excellent":
                return f"🎯 총 {count}명의 최우수 후보를 찾았어요! 평균 매칭률이 {avg_score:.0f}%로 매우 높습니다."
            elif quality_level == "good":
                return f"👍 {count}명의 우수한 후보가 있어요. 평균 매칭률 {avg_score:.0f}%로 좋은 결과입니다."
            else:
                return f"🤔 {count}명의 후보가 있지만, 평균 매칭률이 {avg_score:.0f}%로 추가 검토가 필요해요."
                
        except Exception as e:
            logger.warning(f"요약 메시지 생성 오류: {e}")
            return "검색 결과를 정리해드렸어요."
    
    def _create_fallback_recommendation(self, talent: Dict, rank: int) -> Dict:
        """기본 추천 정보 생성"""
        return {
            "id": talent.get("id", f"talent_{rank}"),
            "name": talent.get("name", f"인재 {rank}"),
            "rank": rank,
            "age": talent.get("age", 30),
            "residence": talent.get("residence", "서울"),
            "specialization": talent.get("specialization", "일반"),
            "experience": f"{talent.get('experience_years', 0)}년",
            "skills": talent.get("skills", [])[:4] if talent.get("skills") else [],
            "score": 80,
            "recommendation": "해당 분야의 경험을 가진 인재입니다.",
            "strengths": ["전문성"],
            "considerations": []
        }
    
    def _generate_error_response(self) -> Dict:
        """오류 응답 생성"""
        return {
            "response_type": "error",
            "message": "😅 죄송해요. 검색 중에 문제가 발생했어요. 다시 시도해주세요.",
            "chatbot_tone": "apologetic",
            "next_actions": [
                "잠시 후 다시 시도해주세요",
                "검색 조건을 다시 확인해보세요",
                "문제가 계속되면 관리자에게 문의해주세요"
            ]
        }
    
    def generate_follow_up_questions(self, response_data: Dict) -> List[str]:
        """후속 질문 생성"""
        try:
            response_type = response_data.get("response_type", "")
            questions = []
            
            if response_type == "recommend":
                questions = [
                    "이 중에서 어떤 분이 가장 관심 있으신가요?",
                    "더 자세한 정보가 필요한 후보가 있나요?",
                    "면접 일정을 잡기 전에 궁금한 점이 있으시나요?"
                ]
            elif response_type == "conditional_recommend":
                questions = [
                    "어떤 조건을 조정하시겠어요?",
                    "현재 후보들 중에서 면접해볼 분이 있나요?",
                    "다른 조건으로 재검색해볼까요?"
                ]
            elif response_type == "suggest_alternatives":
                questions = [
                    "어떤 조건이 가장 중요하신가요?",
                    "경력 조건을 조금 낮춰볼까요?",
                    "지역 범위를 넓혀서 다시 찾아볼까요?"
                ]
            elif response_type == "no_results":
                questions = [
                    "어떤 조건을 가장 먼저 완화해보시겠어요?",
                    "다른 키워드로 검색해볼까요?",
                    "유사한 분야의 인재도 고려하시나요?"
                ]
            
            return questions[:3]
            
        except Exception as e:
            logger.warning(f"후속 질문 생성 오류: {e}")
            return ["다른 도움이 필요하시면 말씀해 주세요!"]
    
    def generate_market_insights(self, parsed_query: Dict, matching_analysis: Dict) -> Dict:
        """시장 인사이트 생성"""
        try:
            insights = {
                "market_status": "",
                "demand_level": "",
                "salary_range": "",
                "recommendations": []
            }
            
            # 전문분야별 시장 상황
            specialization = parsed_query.get("specialization")
            if specialization == "보안":
                insights["market_status"] = "정보보안 전문가는 현재 공급 부족 상태입니다"
                insights["demand_level"] = "매우 높음"
                insights["salary_range"] = "상위 30% 수준"
            elif specialization == "NE":
                insights["market_status"] = "네트워크 엔지니어는 안정적인 수요가 있습니다"
                insights["demand_level"] = "높음"
                insights["salary_range"] = "중상위 수준"
            elif specialization == "DBA":
                insights["market_status"] = "데이터베이스 전문가는 경험자 위주로 선호됩니다"
                insights["demand_level"] = "보통"
                insights["salary_range"] = "상위 수준"
            else:
                insights["market_status"] = "해당 분야는 꾸준한 수요가 있습니다"
                insights["demand_level"] = "보통"
                insights["salary_range"] = "시장 평균"
            
            # 추천사항
            if matching_analysis.get("top_score", 0) < 70:
                insights["recommendations"] = [
                    "조건을 완화하여 인재풀 확대를 권장합니다",
                    "장기적 관점에서 인재 육성을 고려해보세요",
                    "유사 분야 경험자의 전환 교육도 방법입니다"
                ]
            
            return insights
            
        except Exception as e:
            logger.warning(f"시장 인사이트 생성 오류: {e}")
            return {"market_status": "시장 분석 정보를 준비 중입니다."}

# 기존 generator.py와의 호환성을 위한 래퍼 클래스
class RecommendationGenerator(ChatbotRecommendationGenerator):
    """기존 인터페이스 호환성 유지를 위한 래퍼"""
    
    def generate_recommendations(self, user_query: str, parsed_query: Dict, 
                               ranked_talents: List[Dict]) -> List[Dict]:
        """기존 형식으로 응답 변환"""
        try:
            # 챗봇 응답 생성
            chatbot_response = self.generate_chatbot_response(user_query, parsed_query, ranked_talents)
            
            # 기존 형식으로 변환
            if chatbot_response.get("response_type") in ["recommend", "conditional_recommend"]:
                return chatbot_response.get("recommendations", [])
            else:
                # 추천하지 않는 경우 빈 리스트 반환
                return []
                
        except Exception as e:
            logger.error(f"기존 형식 변환 오류: {e}")
            return []
    
    def generate_chatbot_recommendations(self, user_query: str, parsed_query: Dict, 
                                       ranked_talents: List[Dict]) -> Dict:
        """새로운 챗봇 형식 응답"""
        return self.generate_chatbot_response(user_query, parsed_query, ranked_talents)