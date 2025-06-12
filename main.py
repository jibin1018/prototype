"""
인재 검색 웹 서버 메인 파일 - 챗봇 형식 지원
"""

from flask import Flask, render_template, request, jsonify
import json
import sys
import os
from datetime import datetime
import traceback

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # 로컬 모듈 import
    from rulebase_prompt import RulebasePromptParser
    from LLM import LLMParser
    from weight import WeightController
    from payload_search import PayloadSearcher
    from vector_search import VectorSearcher
    from reranking import ReRanker
    from generator import ChatbotRecommendationGenerator  # 새로운 챗봇 생성기
    print("✅ 모든 모듈 import 성공")
except ImportError as e:
    print(f"❌ 모듈 import 오류: {e}")
    print("현재 디렉토리:", os.getcwd())
    print("Python 경로:", sys.path)

app = Flask(__name__)

class TalentSearchSystem:
    """인재 검색 시스템 메인 클래스 - 챗봇 지원"""
    
    def __init__(self, use_llm=False):
        self.use_llm = use_llm
        self.current_year = datetime.now().year
        
        try:
            # 파서 초기화 (rulebase 우선, LLM은 추후 전환)
            if use_llm:
                self.parser = LLMParser()
                print("🤖 LLM 파서 모드 활성화")
            else:
                self.parser = RulebasePromptParser()
                print("📋 Rulebase 파서 모드 활성화")
            
            # 시스템 구성요소 초기화
            self.weight_controller = WeightController()
            self.payload_searcher = PayloadSearcher()
            self.vector_searcher = VectorSearcher()
            self.reranker = ReRanker()
            self.chatbot_generator = ChatbotRecommendationGenerator()  # 챗봇 생성기
            
            print(f"✅ 챗봇 인재 검색 시스템 초기화 완료 (기준년도: {self.current_year})")
            
        except Exception as e:
            print(f"❌ 시스템 초기화 오류: {e}")
            print(traceback.format_exc())
            raise e
    
    def search_talents_chatbot(self, user_query: str):
        """챗봇 형식 인재 검색 메인 로직"""
        try:
            print(f"\n🤖 챗봇 인재 검색 시작: {user_query}")
            
            # 1. 사용자 질의 파싱
            parsed_query = self.parser.parse(user_query)
            print("✅ 1단계: 질의 파싱 완료")
            print(f"파싱 결과: {parsed_query}")
            
            # 2. 가중치 계산
            dynamic_weights = self.weight_controller.calculate_weights(parsed_query)
            print("✅ 2단계: 동적 가중치 계산 완료")
            
            # 3. Payload 검색 (1차 필터링)
            payload_candidates = self.payload_searcher.search(parsed_query)
            print(f"✅ 3단계: Payload 검색 완료 ({len(payload_candidates)}명 후보)")
            
            # 4. 벡터 검색 (2차 정밀 검색)
            vector_results = self.vector_searcher.search(
                parsed_query, payload_candidates
            )
            print(f"✅ 4단계: 벡터 검색 완료 ({len(vector_results)}명 매칭)")
            
            # 5. 재순위화 (가중치 적용)
            ranked_talents = self.reranker.rerank(
                vector_results, dynamic_weights
            )
            print("✅ 5단계: 재순위화 완료")
            
            # 6. 챗봇 형식 응답 생성
            chatbot_response = self.chatbot_generator.generate_chatbot_response(
                user_query, parsed_query, ranked_talents
            )
            print("✅ 6단계: 챗봇 응답 생성 완료")
            
            # 7. 후속 질문 생성
            follow_up_questions = self.chatbot_generator.generate_follow_up_questions(chatbot_response)
            chatbot_response["follow_up_questions"] = follow_up_questions
            
            # 8. 시장 인사이트 생성 (옵션)
            if chatbot_response.get("response_type") in ["suggest_alternatives", "no_results"]:
                market_insights = self.chatbot_generator.generate_market_insights(parsed_query, 
                    chatbot_response.get("matching_analysis", {}))
                chatbot_response["market_insights"] = market_insights
            
            return {
                "success": True,
                "parsed_query": parsed_query,
                "weights": dynamic_weights,
                "total_candidates": len(payload_candidates),
                "matched_talents": len(vector_results),
                "chatbot_response": chatbot_response,
                "recommendations": chatbot_response.get("recommendations", [])  # 기존 호환성
            }
            
        except Exception as e:
            print(f"❌ 챗봇 인재 검색 오류: {str(e)}")
            print(traceback.format_exc())
            return {
                "success": False,
                "error": str(e),
                "chatbot_response": self._generate_error_chatbot_response(str(e)),
                "recommendations": []
            }
    
    def _generate_error_chatbot_response(self, error_message: str) -> dict:
        """오류 시 챗봇 응답 생성"""
        return {
            "response_type": "error",
            "message": f"😅 죄송해요. 검색 중 문제가 발생했어요: {error_message}",
            "summary": "잠시 후 다시 시도해주세요.",
            "chatbot_tone": "apologetic",
            "next_actions": [
                "잠시 후 다시 시도해주세요",
                "검색 조건을 다시 확인해보세요",
                "문제가 계속되면 관리자에게 문의해주세요"
            ]
        }
    
    def search_talents_legacy(self, user_query: str):
        """기존 형식 인재 검색 (호환성 유지)"""
        try:
            result = self.search_talents_chatbot(user_query)
            
            # 챗봇 응답에서 기존 형식으로 변환
            if result["success"] and result.get("chatbot_response"):
                chatbot_data = result["chatbot_response"]
                
                # 추천이 있는 경우만 recommendations에 포함
                if chatbot_data.get("response_type") in ["recommend", "conditional_recommend"]:
                    result["recommendations"] = chatbot_data.get("recommendations", [])
                else:
                    result["recommendations"] = []
            
            return result
            
        except Exception as e:
            print(f"❌ 레거시 검색 오류: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "recommendations": []
            }

# 전역 시스템 인스턴스
try:
    talent_system = TalentSearchSystem(use_llm=False)  # 프로토타입은 rulebase
    print("✅ 전역 시스템 인스턴스 생성 완료")
except Exception as e:
    print(f"❌ 전역 시스템 인스턴스 생성 실패: {e}")
    talent_system = None

@app.route('/')
def index():
    """메인 페이지 - 챗봇 인터페이스"""
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def api_search():
    """인재 검색 API - 챗봇 지원"""
    try:
        if talent_system is None:
            return jsonify({
                "success": False,
                "error": "시스템이 초기화되지 않았습니다.",
                "chatbot_response": {
                    "response_type": "error",
                    "message": "😞 시스템에 문제가 있어요. 관리자에게 문의해주세요.",
                    "chatbot_tone": "apologetic"
                }
            }), 500
            
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "요청 데이터가 없습니다.",
                "chatbot_response": {
                    "response_type": "error",
                    "message": "🤔 요청을 이해할 수 없어요. 다시 말씀해 주시겠어요?",
                    "chatbot_tone": "confused"
                }
            }), 400
            
        user_query = data.get('query', '').strip()
        
        if not user_query:
            return jsonify({
                "success": False,
                "error": "검색 질의가 비어있습니다.",
                "chatbot_response": {
                    "response_type": "error",
                    "message": "🗣️ 어떤 인재를 찾고 계신지 말씀해 주세요!",
                    "chatbot_tone": "encouraging",
                    "next_actions": [
                        "예: 30대 서울 네트워크 엔지니어",
                        "예: 금융권 DBA 5년 이상",
                        "예: 보안 전문가 고급 인재"
                    ]
                }
            }), 400
        
        # 챗봇 형식 인재 검색 실행
        result = talent_system.search_talents_chatbot(user_query)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ API 검색 오류: {e}")
        print(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": f"서버 오류: {str(e)}",
            "chatbot_response": {
                "response_type": "error",
                "message": "😔 서버에 문제가 발생했어요. 잠시 후 다시 시도해주세요.",
                "chatbot_tone": "apologetic",
                "next_actions": ["잠시 후 다시 시도해주세요"]
            }
        }), 500

@app.route('/api/search/legacy', methods=['POST'])
def api_search_legacy():
    """기존 형식 인재 검색 API (호환성 유지)"""
    try:
        if talent_system is None:
            return jsonify({
                "success": False,
                "error": "시스템이 초기화되지 않았습니다."
            }), 500
            
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "요청 데이터가 없습니다."
            }), 400
            
        user_query = data.get('query', '').strip()
        
        if not user_query:
            return jsonify({
                "success": False,
                "error": "검색 질의가 비어있습니다."
            }), 400
        
        # 기존 형식 인재 검색 실행
        result = talent_system.search_talents_legacy(user_query)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ 레거시 API 검색 오류: {e}")
        return jsonify({
            "success": False,
            "error": f"서버 오류: {str(e)}"
        }), 500

@app.route('/api/chat/follow-up', methods=['POST'])
def api_follow_up():
    """후속 질문 처리 API"""
    try:
        data = request.get_json()
        user_input = data.get('input', '').strip()
        context = data.get('context', {})
        
        # 간단한 후속 질문 처리 로직
        # 실제로는 더 정교한 대화 관리가 필요
        
        if "조건" in user_input and "완화" in user_input:
            return jsonify({
                "response": "어떤 조건을 완화하고 싶으신가요? 경력, 지역, 기술스택 중에서 선택해주세요.",
                "suggestions": ["경력 조건 완화", "지역 범위 확대", "기술스택 조건 완화"]
            })
        elif "경력" in user_input and "완화" in user_input:
            return jsonify({
                "response": "경력 조건을 어느 정도로 낮추시겠어요?",
                "suggestions": ["1-2년 낮추기", "3년 이상 낮추기", "경력 무관으로 변경"]
            })
        else:
            return jsonify({
                "response": "더 구체적으로 말씀해 주시겠어요?",
                "suggestions": ["새로운 검색하기", "조건 완화하기", "도움말 보기"]
            })
            
    except Exception as e:
        return jsonify({
            "response": "죄송해요. 이해하지 못했어요. 다시 말씀해 주시겠어요?",
            "error": str(e)
        }), 500

@app.route('/api/switch_parser', methods=['POST'])
def api_switch_parser():
    """파서 모드 전환 API"""
    try:
        data = request.get_json()
        use_llm = data.get('use_llm', False)
        
        global talent_system
        talent_system = TalentSearchSystem(use_llm=use_llm)
        
        parser_type = "LLM" if use_llm else "Rulebase"
        
        return jsonify({
            "success": True,
            "message": f"{parser_type} 파서로 전환되었습니다.",
            "current_parser": parser_type
        })
        
    except Exception as e:
        print(f"❌ 파서 전환 오류: {e}")
        return jsonify({
            "success": False,
            "error": f"파서 전환 오류: {str(e)}"
        }), 500

@app.route('/api/status')
def api_status():
    """시스템 상태 확인"""
    try:
        if talent_system is None:
            return jsonify({
                "system_status": "error",
                "error": "시스템이 초기화되지 않았습니다."
            })
            
        parser_type = "LLM" if talent_system.use_llm else "Rulebase"
        
        return jsonify({
            "system_status": "active",
            "current_parser": parser_type,
            "base_year": talent_system.current_year,
            "mode": "chatbot",
            "components": {
                "parser": "ready",
                "weight_controller": "ready",
                "payload_searcher": "ready", 
                "vector_searcher": "ready",
                "reranker": "ready",
                "chatbot_generator": "ready"
            }
        })
    except Exception as e:
        return jsonify({
            "system_status": "error",
            "error": str(e)
        })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "페이지를 찾을 수 없습니다."}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "내부 서버 오류가 발생했습니다."}), 500

if __name__ == '__main__':
    print("🤖 챗봇 인재 검색 웹 서버 시작")
    print("-" * 50)
    print("📍 URL: http://localhost:5000")
    print("🤖 인터페이스: 챗봇 형식")
    print("🎯 매칭률 기반 지능적 추천")
    
    if talent_system:
        parser_type = "LLM" if talent_system.use_llm else "Rulebase"
        print(f"📋 현재 파서: {parser_type}")
        print("🔄 파서 전환: /api/switch_parser")
    else:
        print("⚠️  시스템 초기화 실패 - 일부 기능이 제한될 수 있습니다")
    
    print("-" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)