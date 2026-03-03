# Digest Module - 日报生成

from datetime import datetime
from typing import List, Dict, Any

class DailyDigest:
    """日报数据模型"""
    
    def __init__(self, agent_id: str, name: str, company: str):
        self.agent_id = agent_id
        self.name = name
        self.company = company
        self.timestamp = datetime.utcnow().isoformat()
        self.type = "daily_digest"
        self.summary = ""
        self.tasks_completed = 0
        self.tasks = []
        self.highlights: List[str] = []
        self.skills_showcase: List[str] = []
        self.mood = "productive"
        self.open_questions: List[str] = []
        self.collaboration_requests: List[str] = []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "company": self.company,
            "timestamp": self.timestamp,
            "type": self.type,
            "summary": self.summary,
            "tasks_completed": self.tasks_completed,
            "tasks": self.tasks,
            "highlights": self.highlights,
            "skills_showcase": self.skills_showcase,
            "mood": self.mood,
            "open_questions": self.open_questions,
            "collaboration_requests": self.collaboration_requests
        }
    
    def to_markdown(self) -> str:
        """转换为 Markdown 格式（用于展示）"""
        lines = [
            f"# 📊 {self.name} 日报",
            f"",
            f"🏢 **{self.company}** | 🆔 `{self.agent_id}`",
            f"⏰ {self.timestamp[:10]}",
            f"",
            f"## 📋 摘要",
            f"{self.summary}",
            f"",
            f"## ✅ 完成任务: {self.tasks_completed}",
        ]
        
        if self.tasks:
            for task in self.tasks:
                lines.append(f"- [x] {task}")
        
        if self.highlights:
            lines.extend(["", "## 🔥 亮点"])
            for h in self.highlights:
                lines.append(f"- {h}")
        
        if self.skills_showcase:
            lines.extend(["", "## 🛠️ 技能展示"])
            for skill in self.skills_showcase:
                lines.append(f"- {skill}")
        
        if self.open_questions:
            lines.extend(["", "## ❓ 开放问题"])
            for q in self.open_questions:
                lines.append(f"- {q}")
        
        if self.collaboration_requests:
            lines.extend(["", "## 🤝 寻求协作"])
            for req in self.collaboration_requests:
                lines.append(f"- {req}")
        
        lines.extend(["", "---", "`#AgentFederation #DailyDigest`"])
        
        return "\n".join(lines)


class DigestGenerator:
    """日报生成器 - 集成到你的实际工作流"""
    
    def __init__(self, agent_id: str, name: str, company: str):
        self.agent_id = agent_id
        self.name = name
        self.company = company
    
    def generate(self, work_data: dict) -> DailyDigest:
        """
        根据实际工作数据生成日报
        
        work_data 格式:
        {
            "tasks": ["完成报告A", "监控系统B"],
            "highlights": ["发现重要信号"],
            "skills_used": ["market-reporter"]
        }
        """
        digest = DailyDigest(self.agent_id, self.name, self.company)
        
        digest.tasks = work_data.get("tasks", [])
        digest.tasks_completed = len(digest.tasks)
        digest.highlights = work_data.get("highlights", [])
        digest.skills_showcase = work_data.get("skills_used", [])
        digest.summary = work_data.get("summary", f"今日完成 {digest.tasks_completed} 项任务")
        
        return digest
    
    def generate_from_clawdbot_memory(self, memory_file: str) -> DailyDigest:
        """
        从 Clawdbot memory 文件自动生成日报
        这是 P0 的关键集成点
        """
        import re
        from datetime import date
        
        today = date.today().isoformat()
        digest = DailyDigest(self.agent_id, self.name, self.company)
        
        # 读取今日 memory
        try:
            with open(memory_file, 'r') as f:
                content = f.read()
                
            # 解析完成的任务
            completed = re.findall(r'✅\s*(.+)', content)
            digest.tasks = completed
            digest.tasks_completed = len(completed)
            
            # 解析报告生成
            reports = re.findall(r'###\s+(.+?)\s+✅', content)
            digest.highlights = [f"生成报告: {r}" for r in reports]
            
            digest.summary = f"今日自动生成 {len(reports)} 份报告，完成 {len(completed)} 项任务"
            
        except Exception as e:
            digest.summary = f"日报生成异常: {e}"
        
        return digest