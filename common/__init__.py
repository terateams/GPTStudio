ExamCategorys = [
    "",
    "微软 AI-900",
    "Mikrotik 认证",
    "Python 编程",
    "初中数学",
    "初中物理",
    "初中生物",
    "初中英语",
    "初中历史",
    "初中地理",
    "初中政治",
]

ExamSchema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "id": {"type": "string", "description": "题目的唯一标识符"},
        "question": {"type": "string", "description": "题目内容"},
        "options": {
            "type": "array",
            "description": "题目的选项列表",
            "items": {
                "type": "object",
                "minProperties": 1,
                "maxProperties": 1,
                "additionalProperties": {"type": "string"},
            },
            "minItems": 4,
            "maxItems": 4,
        },
        "correct_answer": {
            "type": "array",
            "items": {"type": "string"},
            "description": "正确答案的选项标识符 ABCD 中的一个或多个",
        },
        "selection_mode": {"type": "string", "description": "选择模式 single 或 multi"},
        "category": {"type": "string", "description": "题目所属分类"},
        "user_code": {"type": "string", "description": "用户编号, 代表用户专有试题"},
        "difficulty": {
            "type": "string",
            "description": "题目难度",
            "enum": ["简单", "中等", "困难"],
        },
        "tags": {
            "type": "array",
            "items": {"type": "string"},
            "description": "题目标签",
        },
        "explanation": {"type": "string", "description": "答案解析"},
        "source": {"type": "string", "description": "题目来源"},
        "imgb64": {"type": "string", "description": "题目图片的 Base64 编码"},
        "img_url": {"type": "string", "description": "题目图片URL"},
        "created_at": {
            "type": "string",
            "description": "题目创建时间，ISO 8601 格式",
            "format": "date-time",
        },
    },
    "required": [
        "id",
        "question",
        "options",
        "correct_answer",
        "selection_mode",
        "category",
        "difficulty",
        "tags",
        "explanation",
        "source",
        "created_at",
    ],
    "additionalProperties": False,
}


ExamArraySchema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "description": "包含多个题目的对象",
    "properties": {
        "title": {
            "type": "string",
            "description": "根据内容生成试题集标题,可用作文件名",
        },
        "exams": {
            "type": "array",
            "description": "题目数组",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "题目的唯一标识符"},
                    "question": {"type": "string", "description": "题目内容"},
                    "options": {
                        "type": "array",
                        "description": "题目的选项列表",
                        "items": {
                            "type": "object",
                            "minProperties": 1,
                            "maxProperties": 1,
                            "additionalProperties": {"type": "string"},
                        },
                        "minItems": 4,
                        "maxItems": 4,
                    },
                    "correct_answer": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "正确答案的选项标识符 ABCD 中的一个或多个",
                    },
                    "selection_mode": {
                        "type": "string",
                        "description": "选择模式 single 或 multi",
                    },
                    "category": {"type": "string", "description": "题目所属分类"},
                    "user_code": {
                        "type": "string",
                        "description": "用户编号, 代表用户专有试题, 默认使用 global",
                    },
                    "difficulty": {
                        "type": "string",
                        "description": "题目难度",
                        "enum": ["简单", "中等", "困难"],
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "题目标签",
                    },
                    "explanation": {"type": "string", "description": "答案解析"},
                    "source": {"type": "string", "description": "题目来源"},
                    "imgb64": {
                        "type": "string",
                        "description": "题目图片的 Base64 编码",
                    },
                    "img_url": {"type": "string", "description": "题目图片URL"},
                    "created_at": {
                        "type": "string",
                        "description": "题目创建时间，ISO 8601 格式",
                        "format": "date-time",
                    },
                },
                "required": [
                    "id",
                    "question",
                    "options",
                    "correct_answer",
                    "selection_mode",
                    "category",
                    "difficulty",
                    "tags",
                    "explanation",
                    "source",
                    "created_at",
                ],
                "additionalProperties": False,
            },
            "minItems": 1,
            "maxItems": 50,
        },
    },
    "required": ["exams"],
    "additionalProperties": False,
}



ExamQASchema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "id": {"type": "string", "description": "题目的唯一标识符"},
        "question": {"type": "string", "description": "题目内容"},
        "answer": {
            "type": "string",
            "description": "问题的答案",
        },
        "category": {"type": "string", "description": "题目所属分类"},
        "user_code": {"type": "string", "description": "用户编号, 代表用户专有试题, 默认使用 global"},
        "difficulty": {
            "type": "string",
            "description": "题目难度",
            "enum": ["简单", "中等", "困难"],
        },
        "tags": {
            "type": "array",
            "items": {"type": "string"},
            "description": "题目标签",
        },
        "explanation": {"type": "string", "description": "答案解析"},
        "source": {"type": "string", "description": "题目来源"},
        "imgb64": {"type": "string", "description": "题目图片的 Base64 编码"},
        "img_url": {"type": "string", "description": "题目图片URL"},
        "created_at": {
            "type": "string",
            "description": "题目创建时间，ISO 8601 格式",
            "format": "date-time",
        },
    },
    "required": [
        "id",
        "question",
        "answer",
        "category",
        "difficulty",
        "tags",
        "explanation",
        "source",
        "created_at",
    ],
    "additionalProperties": False,
}



ExamQAArraySchema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "description": "包含多个题目的对象",
    "properties": {
        "title": {
            "type": "string",
            "description": "根据内容生成试题集标题,可用作文件名",
        },
        "exams": {
            "type": "array",
            "description": "题目数组",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "题目的唯一标识符"},
                    "question": {"type": "string", "description": "题目内容"},
                    "answer": {
                        "type": "string",
                        "items": {"type": "string"},
                        "description": "问题的答案",
                    },
                    "category": {"type": "string", "description": "题目所属分类"},
                    "user_code": {
                        "type": "string",
                        "description": "用户编号, 代表用户专有试题, 默认使用 global",
                    },
                    "difficulty": {
                        "type": "string",
                        "description": "题目难度",
                        "enum": ["简单", "中等", "困难"],
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "题目标签",
                    },
                    "explanation": {"type": "string", "description": "答案解析"},
                    "source": {"type": "string", "description": "题目来源"},
                    "imgb64": {
                        "type": "string",
                        "description": "题目图片的 Base64 编码",
                    },
                    "img_url": {"type": "string", "description": "题目图片URL"},
                    "created_at": {
                        "type": "string",
                        "description": "题目创建时间，ISO 8601 格式",
                        "format": "date-time",
                    },
                },
                "required": [
                    "id",
                    "question",
                    "options",
                    "answer",
                    "category",
                    "difficulty",
                    "tags",
                    "explanation",
                    "source",
                    "created_at",
                ],
                "additionalProperties": False,
            },
            "minItems": 1,
            "maxItems": 50,
        },
    },
    "required": ["exams"],
    "additionalProperties": False,
}
