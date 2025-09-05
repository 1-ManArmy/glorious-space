from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn
import random
import datetime
import json
import re

app = FastAPI(title="Content Creator Ace Agent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContentRequest(BaseModel):
    content_type: str  # "social_post", "blog", "email", "ad_copy", "video_script"
    topic: str
    platform: Optional[str] = None  # "instagram", "twitter", "linkedin", "facebook", "tiktok"
    tone: Optional[str] = "engaging"  # "professional", "casual", "funny", "inspiring"
    target_audience: Optional[str] = None
    word_count: Optional[int] = None
    keywords: Optional[List[str]] = []

class GeneratedContent(BaseModel):
    content: str
    content_type: str
    platform: str
    hashtags: List[str]
    engagement_tips: List[str]
    best_posting_times: List[str]
    call_to_action: str
    performance_prediction: str

class ContentCreatorAce:
    def __init__(self):
        self.name = "Content Creator Ace"
        self.specialty = "Multi-platform content creation and social media strategy"
        
        self.platform_specs = {
            "instagram": {
                "max_chars": 2200,
                "optimal_hashtags": 10,
                "content_style": "Visual-first, story-driven, authentic",
                "best_times": ["6-9 AM", "12-2 PM", "5-7 PM"],
                "engagement_focus": "Stories, Reels, carousel posts"
            },
            "twitter": {
                "max_chars": 280,
                "optimal_hashtags": 3,
                "content_style": "Concise, timely, conversational",
                "best_times": ["9-10 AM", "12-1 PM", "5-6 PM"],
                "engagement_focus": "Threads, polls, replies"
            },
            "linkedin": {
                "max_chars": 3000,
                "optimal_hashtags": 5,
                "content_style": "Professional, value-driven, thought leadership",
                "best_times": ["8-10 AM", "12-2 PM", "5-6 PM"],
                "engagement_focus": "Articles, professional insights, industry news"
            },
            "facebook": {
                "max_chars": 63206,
                "optimal_hashtags": 5,
                "content_style": "Community-focused, storytelling, relatable",
                "best_times": ["9 AM-12 PM", "1-3 PM", "7-9 PM"],
                "engagement_focus": "Videos, community posts, events"
            },
            "tiktok": {
                "max_chars": 4000,
                "optimal_hashtags": 8,
                "content_style": "Trendy, entertaining, authentic",
                "best_times": ["6-10 AM", "7-9 PM"],
                "engagement_focus": "Short videos, trending sounds, challenges"
            }
        }
        
        self.content_templates = {
            "social_post": {
                "hooks": [
                    "🚨 This changes everything:",
                    "💡 Here's what nobody tells you about",
                    "🔥 Hot take:",
                    "📈 Just discovered:",
                    "⚡ Quick reminder:",
                    "🎯 Pro tip:",
                    "🌟 Today I learned:",
                    "💎 Hidden gem alert:"
                ],
                "structures": [
                    "Hook → Value → Call to Action",
                    "Question → Answer → Engagement",
                    "Story → Lesson → Application",
                    "Problem → Solution → Benefit"
                ]
            },
            "blog": {
                "intros": [
                    "Have you ever wondered why",
                    "In today's fast-paced world,",
                    "The secret to success in",
                    "What if I told you that",
                    "Most people don't realize",
                    "Here's the truth about"
                ],
                "structures": [
                    "Introduction → Main Points → Conclusion",
                    "Problem → Solution → Benefits → Action",
                    "Story → Insights → Application → CTA"
                ]
            }
        }
        
        self.hashtag_categories = {
            "business": ["#entrepreneurship", "#business", "#startup", "#success", "#leadership", "#productivity", "#growth", "#innovation"],
            "technology": ["#tech", "#AI", "#innovation", "#digital", "#future", "#automation", "#software", "#coding"],
            "lifestyle": ["#lifestyle", "#motivation", "#inspiration", "#selfcare", "#wellness", "#mindset", "#goals", "#happiness"],
            "education": ["#learning", "#education", "#knowledge", "#skills", "#development", "#training", "#tips", "#tutorial"],
            "marketing": ["#marketing", "#socialmedia", "#content", "#branding", "#digital", "#strategy", "#advertising", "#growth"],
            "finance": ["#finance", "#money", "#investing", "#wealth", "#financial", "#savings", "#budget", "#crypto"]
        }
        
        self.tone_styles = {
            "professional": {
                "vocabulary": "industry-specific, formal, authoritative",
                "sentence_structure": "complex, well-structured",
                "examples": ["leverage", "optimize", "implement", "strategic", "comprehensive"]
            },
            "casual": {
                "vocabulary": "everyday, conversational, relatable",
                "sentence_structure": "simple, informal",
                "examples": ["hey", "awesome", "super", "totally", "amazing"]
            },
            "funny": {
                "vocabulary": "humorous, playful, witty",
                "sentence_structure": "punchy, unexpected",
                "examples": ["plot twist", "spoiler alert", "mic drop", "no cap", "periodt"]
            },
            "inspiring": {
                "vocabulary": "motivational, uplifting, empowering",
                "sentence_structure": "rhythmic, impactful",
                "examples": ["believe", "achieve", "transform", "overcome", "breakthrough"]
            }
        }

    def generate_content(self, request: ContentRequest) -> GeneratedContent:
        platform = request.platform or "instagram"
        platform_info = self.platform_specs.get(platform, self.platform_specs["instagram"])
        
        # Generate main content based on type
        if request.content_type == "social_post":
            content = self.create_social_post(request, platform_info)
        elif request.content_type == "blog":
            content = self.create_blog_post(request)
        elif request.content_type == "email":
            content = self.create_email_content(request)
        elif request.content_type == "ad_copy":
            content = self.create_ad_copy(request)
        elif request.content_type == "video_script":
            content = self.create_video_script(request, platform_info)
        else:
            content = self.create_social_post(request, platform_info)
        
        # Generate hashtags
        hashtags = self.generate_hashtags(request.topic, request.keywords, platform)
        
        # Generate engagement tips
        engagement_tips = self.get_engagement_tips(platform, request.content_type)
        
        # Generate call to action
        cta = self.generate_cta(request.content_type, platform)
        
        # Predict performance
        performance = self.predict_performance(request, platform)
        
        return GeneratedContent(
            content=content,
            content_type=request.content_type,
            platform=platform,
            hashtags=hashtags,
            engagement_tips=engagement_tips,
            best_posting_times=platform_info["best_times"],
            call_to_action=cta,
            performance_prediction=performance
        )
    
    def create_social_post(self, request: ContentRequest, platform_info: Dict) -> str:
        hook = random.choice(self.content_templates["social_post"]["hooks"])
        
        if request.tone == "professional":
            post = f"{hook} {request.topic}\n\n"
            post += f"In today's competitive landscape, understanding {request.topic} is crucial for success. "
            post += f"Here's what industry leaders are implementing:\n\n"
            post += f"✅ Strategic approach to {request.topic}\n"
            post += f"✅ Measurable outcomes and ROI\n"
            post += f"✅ Best practices from market leaders\n\n"
            post += f"What's your experience with {request.topic}? Share below! 👇"
            
        elif request.tone == "casual":
            post = f"Okay, let's talk about {request.topic} for a sec 👀\n\n"
            post += f"So basically, everyone's been asking me about this lately and honestly? "
            post += f"It's way simpler than people make it out to be.\n\n"
            post += f"Here's the tea ☕:\n"
            post += f"• It's all about [key point 1]\n"
            post += f"• Don't overthink [key point 2]\n"
            post += f"• Just start with [key point 3]\n\n"
            post += f"Trust me on this one. What do you think? 💭"
            
        elif request.tone == "funny":
            post = f"POV: You finally understand {request.topic} 🤯\n\n"
            post += f"Me before: *confused screaming*\n"
            post += f"Me now: *still confused but with confidence*\n\n"
            post += f"But seriously, {request.topic} doesn't have to be rocket science 🚀\n\n"
            post += f"Here's what actually works:\n"
            post += f"1. Stop overthinking it\n"
            post += f"2. Start somewhere (anywhere!)\n"
            post += f"3. Learn as you go\n\n"
            post += f"Who else can relate? 😅"
            
        else:  # inspiring
            post = f"✨ Your reminder that {request.topic} is within your reach ✨\n\n"
            post += f"Every expert was once a beginner. Every success story started with a single step.\n\n"
            post += f"Today, you have the power to:\n"
            post += f"🌟 Transform your approach to {request.topic}\n"
            post += f"🌟 Overcome any obstacles in your path\n"
            post += f"🌟 Create the breakthrough you've been waiting for\n\n"
            post += f"Your journey starts now. Are you ready? 💪"
        
        return post
    
    def create_blog_post(self, request: ContentRequest) -> str:
        intro = random.choice(self.content_templates["blog"]["intros"])
        
        blog_post = f"# The Ultimate Guide to {request.topic}\n\n"
        blog_post += f"{intro} {request.topic}? You're not alone. "
        blog_post += f"In this comprehensive guide, we'll explore everything you need to know about {request.topic} "
        blog_post += f"and how it can transform your approach to success.\n\n"
        
        blog_post += f"## Why {request.topic} Matters Now More Than Ever\n\n"
        blog_post += f"The landscape is changing rapidly, and {request.topic} has become a crucial factor in "
        blog_post += f"determining success in today's competitive environment.\n\n"
        
        blog_post += f"## Key Strategies for Mastering {request.topic}\n\n"
        blog_post += f"### 1. Foundation Building\n"
        blog_post += f"Start with a solid understanding of the fundamentals...\n\n"
        blog_post += f"### 2. Implementation Tactics\n"
        blog_post += f"Here's how to put theory into practice...\n\n"
        blog_post += f"### 3. Advanced Techniques\n"
        blog_post += f"Once you've mastered the basics, elevate your approach with...\n\n"
        
        blog_post += f"## Common Mistakes to Avoid\n\n"
        blog_post += f"Learn from others' experiences and sidestep these pitfalls...\n\n"
        
        blog_post += f"## Your Next Steps\n\n"
        blog_post += f"Ready to implement what you've learned? Start with these actionable steps...\n\n"
        blog_post += f"What's your experience with {request.topic}? Share your thoughts in the comments below!"
        
        return blog_post
    
    def create_email_content(self, request: ContentRequest) -> str:
        subject_line = f"🔥 The {request.topic} breakthrough you've been waiting for"
        
        email = f"Subject: {subject_line}\n\n"
        email += f"Hey there!\n\n"
        email += f"Quick question: What if I told you that mastering {request.topic} "
        email += f"could be the game-changer you've been looking for?\n\n"
        email += f"I know, I know – you've probably heard that before. But here's the thing...\n\n"
        email += f"Most people approach {request.topic} completely wrong.\n\n"
        email += f"They focus on [common mistake] instead of [correct approach].\n\n"
        email += f"That's why I put together this exclusive guide that shows you exactly how to:\n\n"
        email += f"✅ [Benefit 1]\n"
        email += f"✅ [Benefit 2]\n"
        email += f"✅ [Benefit 3]\n\n"
        email += f"Want to check it out?\n\n"
        email += f"[DOWNLOAD YOUR FREE GUIDE]\n\n"
        email += f"Talk soon,\n"
        email += f"[Your Name]"
        
        return email
    
    def create_ad_copy(self, request: ContentRequest) -> str:
        headline = f"Finally! The {request.topic} Solution Everyone's Talking About"
        
        ad_copy = f"HEADLINE: {headline}\n\n"
        ad_copy += f"Are you tired of struggling with {request.topic}?\n\n"
        ad_copy += f"What if there was a proven system that could help you master {request.topic} "
        ad_copy += f"in just [timeframe]?\n\n"
        ad_copy += f"Introducing [Product/Service Name] – the breakthrough solution that's helped "
        ad_copy += f"thousands of people transform their approach to {request.topic}.\n\n"
        ad_copy += f"✅ Get results in just [timeframe]\n"
        ad_copy += f"✅ No prior experience needed\n"
        ad_copy += f"✅ 100% satisfaction guarantee\n\n"
        ad_copy += f"Limited time offer: Save 50% when you act now!\n\n"
        ad_copy += f"[CLAIM YOUR DISCOUNT NOW]\n\n"
        ad_copy += f"*Offer expires in 24 hours"
        
        return ad_copy
    
    def create_video_script(self, request: ContentRequest, platform_info: Dict) -> str:
        if platform_info == self.platform_specs["tiktok"]:
            return self.create_tiktok_script(request)
        else:
            return self.create_general_video_script(request)
    
    def create_tiktok_script(self, request: ContentRequest) -> str:
        script = f"🎬 TikTok Video Script: {request.topic}\n\n"
        script += f"[HOOK - First 3 seconds]\n"
        script += f"*Text overlay: \"POV: You finally understand {request.topic}\"*\n"
        script += f"*Trending sound plays*\n\n"
        script += f"[CONTENT - 15-30 seconds]\n"
        script += f"*Quick cuts showing before/after*\n"
        script += f"*Text overlays with key points*\n"
        script += f"• Point 1 about {request.topic}\n"
        script += f"• Point 2 about {request.topic}\n"
        script += f"• Point 3 about {request.topic}\n\n"
        script += f"[CTA - Last 5 seconds]\n"
        script += f"*Text overlay: \"Follow for more tips!\"*\n"
        script += f"*Pointing gesture to follow button*\n\n"
        script += f"CAPTION: Check comments for full guide! 👇"
        
        return script
    
    def create_general_video_script(self, request: ContentRequest) -> str:
        script = f"📹 Video Script: {request.topic}\n\n"
        script += f"[INTRO - 0:00-0:15]\n"
        script += f"\"Hey everyone! Today we're diving deep into {request.topic}. "
        script += f"If you've been struggling with this, you're in the right place.\"\n\n"
        script += f"[MAIN CONTENT - 0:15-2:30]\n"
        script += f"\"Let me share the three most important things about {request.topic}:\n\n"
        script += f"First... [Key Point 1]\n"
        script += f"Second... [Key Point 2]\n"
        script += f"And finally... [Key Point 3]\"\n\n"
        script += f"[CONCLUSION - 2:30-3:00]\n"
        script += f"\"So there you have it! Which of these resonated most with you? "
        script += f"Let me know in the comments, and don't forget to subscribe for more content like this!\"\n\n"
        script += f"[END SCREEN - 3:00-3:10]\n"
        script += f"*Subscribe button animation*\n"
        script += f"*Related video thumbnails*"
        
        return script
    
    def generate_hashtags(self, topic: str, keywords: List[str], platform: str) -> List[str]:
        topic_lower = topic.lower()
        hashtags = []
        
        # Add topic-based hashtags
        if "business" in topic_lower or "entrepreneur" in topic_lower:
            hashtags.extend(random.sample(self.hashtag_categories["business"], 3))
        elif "tech" in topic_lower or "ai" in topic_lower:
            hashtags.extend(random.sample(self.hashtag_categories["technology"], 3))
        elif "marketing" in topic_lower:
            hashtags.extend(random.sample(self.hashtag_categories["marketing"], 3))
        else:
            hashtags.extend(random.sample(self.hashtag_categories["lifestyle"], 3))
        
        # Add keyword-based hashtags
        for keyword in keywords[:3]:
            hashtags.append(f"#{keyword.replace(' ', '').lower()}")
        
        # Add platform-specific hashtags
        platform_hashtags = {
            "instagram": ["#instadaily", "#explore", "#viral"],
            "tiktok": ["#fyp", "#foryou", "#viral"],
            "linkedin": ["#professional", "#career", "#business"],
            "twitter": ["#trending", "#discussion", "#thoughts"]
        }
        
        hashtags.extend(platform_hashtags.get(platform, []))
        
        # Limit to platform optimal count
        max_hashtags = self.platform_specs[platform]["optimal_hashtags"]
        return hashtags[:max_hashtags]
    
    def get_engagement_tips(self, platform: str, content_type: str) -> List[str]:
        general_tips = [
            "Ask questions in your captions to encourage comments",
            "Respond to all comments within the first hour",
            "Use strong visuals that stop the scroll",
            "Include clear call-to-actions"
        ]
        
        platform_specific = {
            "instagram": [
                "Use Instagram Stories polls and questions",
                "Post carousel content for higher engagement",
                "Share behind-the-scenes content",
                "Use location tags and relevant hashtags"
            ],
            "tiktok": [
                "Jump on trending sounds and hashtags",
                "Keep videos under 30 seconds for better retention",
                "Use text overlays for accessibility",
                "Post consistently at peak times"
            ],
            "linkedin": [
                "Share professional insights and experiences",
                "Engage with other professionals' content",
                "Use LinkedIn native video",
                "Tag relevant industry connections"
            ]
        }
        
        tips = general_tips + platform_specific.get(platform, [])
        return random.sample(tips, 4)
    
    def generate_cta(self, content_type: str, platform: str) -> str:
        ctas = {
            "social_post": [
                "What's your take on this? Comment below! 👇",
                "Save this post and share with someone who needs to see it!",
                "Double-tap if you agree! ❤️",
                "Which tip will you try first? Let me know!"
            ],
            "blog": [
                "Ready to take action? Download our free guide!",
                "Want more insights like this? Subscribe to our newsletter!",
                "Share this post with your network!",
                "Leave a comment with your thoughts!"
            ],
            "email": [
                "Click here to learn more →",
                "Download your free resource now!",
                "Join thousands of others who've transformed their approach!",
                "Don't miss out – limited time offer!"
            ],
            "video_script": [
                "Subscribe for more content like this!",
                "Hit the like button if this helped you!",
                "Share this video with someone who needs to see it!",
                "What video should I make next? Comment below!"
            ]
        }
        
        return random.choice(ctas.get(content_type, ctas["social_post"]))
    
    def predict_performance(self, request: ContentRequest, platform: str) -> str:
        factors = []
        score = 70  # Base score
        
        # Adjust based on platform
        if platform in ["instagram", "tiktok"]:
            score += 10  # Higher engagement platforms
            
        # Adjust based on content type
        if request.content_type == "video_script":
            score += 15  # Video content performs better
        elif request.content_type == "social_post":
            score += 5
            
        # Adjust based on tone
        if request.tone in ["funny", "inspiring"]:
            score += 10  # Emotional content performs better
            
        # Generate prediction
        if score >= 90:
            return "🔥 High viral potential - expect 3-5x normal engagement"
        elif score >= 80:
            return "📈 Strong performance predicted - above average engagement expected"
        elif score >= 70:
            return "✅ Good performance expected - solid engagement likely"
        else:
            return "📊 Moderate performance - consider optimizing for better results"

# Initialize the Content Creator
content_creator = ContentCreatorAce()

@app.get("/")
async def root():
    return {
        "agent": "Content Creator Ace",
        "version": "1.0.0",
        "description": "AI-powered content creation specialist for all social media platforms and content types",
        "specialties": [
            "Social Media Posts",
            "Blog Articles", 
            "Email Marketing",
            "Ad Copy",
            "Video Scripts",
            "Platform Optimization"
        ],
        "supported_platforms": list(content_creator.platform_specs.keys()),
        "content_types": ["social_post", "blog", "email", "ad_copy", "video_script"],
        "endpoints": {
            "/generate": "POST - Generate content for any platform",
            "/platform-specs": "GET - Get platform specifications",
            "/content-calendar": "POST - Generate content calendar",
            "/trending": "GET - Get trending topics and hashtags"
        }
    }

@app.post("/generate", response_model=GeneratedContent)
async def generate_content(request: ContentRequest):
    try:
        content = content_creator.generate_content(request)
        return content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating content: {str(e)}")

@app.get("/platform-specs")
async def get_platform_specs(platform: str = None):
    if platform:
        return {
            "platform": platform,
            "specs": content_creator.platform_specs.get(platform, "Platform not found")
        }
    return {
        "all_platforms": content_creator.platform_specs
    }

@app.post("/content-calendar")
async def generate_content_calendar(days: int = 7, platforms: List[str] = ["instagram", "twitter"]):
    calendar = {}
    topics = ["productivity", "motivation", "tips", "behind-the-scenes", "education", "inspiration", "trends"]
    
    for day in range(days):
        date = (datetime.datetime.now() + datetime.timedelta(days=day)).strftime("%Y-%m-%d")
        calendar[date] = {}
        
        for platform in platforms:
            topic = random.choice(topics)
            content_type = "social_post"
            
            fake_request = ContentRequest(
                content_type=content_type,
                topic=topic,
                platform=platform,
                tone=random.choice(["engaging", "professional", "inspiring"])
            )
            
            calendar[date][platform] = {
                "topic": topic,
                "content_type": content_type,
                "best_time": random.choice(content_creator.platform_specs[platform]["best_times"]),
                "priority": random.choice(["high", "medium", "low"])
            }
    
    return {
        "calendar": calendar,
        "total_posts": len(platforms) * days,
        "platforms": platforms,
        "duration": f"{days} days"
    }

@app.get("/trending")
async def get_trending_info():
    trending_topics = [
        "AI and automation", "Remote work tips", "Personal branding", 
        "Mental health awareness", "Sustainable living", "Digital detox",
        "Skill development", "Entrepreneurship", "Creative inspiration"
    ]
    
    trending_hashtags = [
        "#MondayMotivation", "#TipTuesday", "#WisdomWednesday", 
        "#ThrowbackThursday", "#FridayFeeling", "#SelfCareSunday",
        "#Mindfulness", "#GrowthMindset", "#Innovation"
    ]
    
    return {
        "trending_topics": trending_topics,
        "trending_hashtags": trending_hashtags,
        "content_ideas": [
            f"Create a post about {topic} using {hashtag}"
            for topic, hashtag in zip(trending_topics[:5], trending_hashtags[:5])
        ],
        "last_updated": datetime.datetime.now().isoformat()
    }

if __name__ == "__main__":
    print("✍️ Starting Content Creator Ace Agent...")
    print("📱 Ready to create amazing content for all platforms!")
    uvicorn.run(app, host="0.0.0.0", port=8007)
