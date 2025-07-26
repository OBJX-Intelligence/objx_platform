# OBJX Intelligence Platform - API Documentation

## Overview

The OBJX Intelligence Platform provides a comprehensive RESTful API that enables integration with external systems, custom applications, and white-label deployments. The API is built on systematic thinking principles and provides access to the platform's core intelligence capabilities.

## Base URL

- **Production**: `https://api.objx.design/v1`
- **Development**: `http://localhost:5000/api`

## Authentication

The API uses JWT (JSON Web Tokens) for authentication with role-based access control.

### Authentication Flow

1. **Login**: Exchange credentials for access token
2. **Request**: Include token in Authorization header
3. **Refresh**: Use refresh token to get new access token

### Login Endpoint

```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password",
  "tenant_id": "optional_tenant_id"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "expires_in": 3600,
  "user": {
    "id": "user_uuid",
    "email": "user@example.com",
    "role": "user",
    "tenant_id": "tenant_uuid"
  }
}
```

### Using Authentication

Include the access token in the Authorization header for all authenticated requests:

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## Core Endpoints

### Chat Intelligence

The chat endpoint provides access to the platform's systematic thinking capabilities.

#### Send Message

```http
POST /chat
Authorization: Bearer <token>
Content-Type: application/json

{
  "message": "Analyze the market trends for renewable energy",
  "context": "quarterly_analysis",
  "metadata": {
    "department": "strategy",
    "priority": "high"
  }
}
```

**Response:**
```json
{
  "id": "conversation_uuid",
  "response": "Based on systematic analysis of renewable energy market trends...",
  "thinking_process": {
    "clarification": "Market trends analysis for renewable energy sector",
    "compound_factors": ["policy changes", "technology advancement", "cost reduction"],
    "creation": "Strategic recommendations based on systematic evaluation"
  },
  "metadata": {
    "response_time": 2.3,
    "tokens_used": 1250,
    "confidence_score": 0.92
  },
  "created_at": "2024-01-24T10:30:00Z"
}
```

#### Get Conversation History

```http
GET /chat/conversations
Authorization: Bearer <token>
```

**Query Parameters:**
- `limit`: Number of conversations to return (default: 20, max: 100)
- `offset`: Pagination offset (default: 0)
- `from_date`: ISO 8601 date string
- `to_date`: ISO 8601 date string

**Response:**
```json
{
  "conversations": [
    {
      "id": "conversation_uuid",
      "created_at": "2024-01-24T10:30:00Z",
      "last_message": "Analyze the market trends for renewable energy",
      "message_count": 5,
      "metadata": {
        "department": "strategy",
        "priority": "high"
      }
    }
  ],
  "total": 150,
  "has_more": true
}
```

#### Get Specific Conversation

```http
GET /chat/conversations/{conversation_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": "conversation_uuid",
  "messages": [
    {
      "id": "message_uuid",
      "role": "user",
      "content": "Analyze the market trends for renewable energy",
      "timestamp": "2024-01-24T10:30:00Z"
    },
    {
      "id": "message_uuid",
      "role": "assistant",
      "content": "Based on systematic analysis...",
      "thinking_process": {
        "clarification": "...",
        "compound_factors": [...],
        "creation": "..."
      },
      "timestamp": "2024-01-24T10:30:15Z"
    }
  ],
  "created_at": "2024-01-24T10:30:00Z",
  "metadata": {
    "department": "strategy",
    "priority": "high"
  }
}
```

### Memory Management

The platform's compound learning system provides persistent memory across conversations.

#### Search Memory

```http
POST /memory/search
Authorization: Bearer <token>
Content-Type: application/json

{
  "query": "renewable energy analysis",
  "limit": 10,
  "filters": {
    "department": "strategy",
    "date_range": {
      "from": "2024-01-01T00:00:00Z",
      "to": "2024-01-31T23:59:59Z"
    }
  }
}
```

**Response:**
```json
{
  "memories": [
    {
      "id": "memory_uuid",
      "content": "Market analysis showed 23% growth in solar installations",
      "context": "quarterly_analysis",
      "relevance_score": 0.95,
      "created_at": "2024-01-15T14:20:00Z",
      "metadata": {
        "source": "conversation",
        "department": "strategy"
      }
    }
  ],
  "total": 25,
  "query_time": 0.15
}
```

#### Add Memory

```http
POST /memory
Authorization: Bearer <token>
Content-Type: application/json

{
  "content": "Key insight: Solar panel efficiency increased 15% this quarter",
  "context": "quarterly_review",
  "metadata": {
    "department": "research",
    "importance": "high",
    "tags": ["solar", "efficiency", "quarterly"]
  }
}
```

**Response:**
```json
{
  "id": "memory_uuid",
  "content": "Key insight: Solar panel efficiency increased 15% this quarter",
  "context": "quarterly_review",
  "created_at": "2024-01-24T10:45:00Z",
  "metadata": {
    "department": "research",
    "importance": "high",
    "tags": ["solar", "efficiency", "quarterly"]
  }
}
```

#### Delete Memory

```http
DELETE /memory/{memory_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Memory deleted successfully",
  "deleted_at": "2024-01-24T10:50:00Z"
}
```

### User Management

#### Get User Profile

```http
GET /user/profile
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": "user_uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "manager",
  "tenant_id": "tenant_uuid",
  "subscription_tier": "compound_intelligence",
  "created_at": "2024-01-01T00:00:00Z",
  "last_active": "2024-01-24T10:30:00Z",
  "preferences": {
    "theme": "dark",
    "notifications": true,
    "language": "en"
  }
}
```

#### Update User Profile

```http
PUT /user/profile
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "John Smith",
  "preferences": {
    "theme": "light",
    "notifications": false,
    "language": "en"
  }
}
```

**Response:**
```json
{
  "id": "user_uuid",
  "email": "user@example.com",
  "name": "John Smith",
  "preferences": {
    "theme": "light",
    "notifications": false,
    "language": "en"
  },
  "updated_at": "2024-01-24T10:55:00Z"
}
```

### Analytics & Insights

#### Usage Analytics

```http
GET /analytics/usage
Authorization: Bearer <token>
```

**Query Parameters:**
- `period`: Time period (day, week, month, quarter, year)
- `from_date`: Start date (ISO 8601)
- `to_date`: End date (ISO 8601)
- `granularity`: Data granularity (hour, day, week, month)

**Response:**
```json
{
  "period": "month",
  "from_date": "2024-01-01T00:00:00Z",
  "to_date": "2024-01-31T23:59:59Z",
  "metrics": {
    "total_conversations": 1250,
    "total_messages": 5680,
    "unique_users": 45,
    "average_response_time": 2.1,
    "memory_entries": 890,
    "api_calls": 12500
  },
  "trends": [
    {
      "date": "2024-01-01",
      "conversations": 35,
      "messages": 156,
      "users": 12
    }
  ]
}
```

#### Intelligence Insights

```http
GET /analytics/insights
Authorization: Bearer <token>
```

**Response:**
```json
{
  "insights": [
    {
      "type": "usage_pattern",
      "title": "Peak Usage Hours",
      "description": "Highest activity between 9-11 AM and 2-4 PM",
      "confidence": 0.89,
      "data": {
        "peak_hours": ["09:00", "10:00", "14:00", "15:00"],
        "usage_distribution": {...}
      }
    },
    {
      "type": "content_analysis",
      "title": "Top Discussion Topics",
      "description": "Most frequent topics in conversations",
      "confidence": 0.92,
      "data": {
        "topics": [
          {"topic": "market analysis", "frequency": 0.23},
          {"topic": "strategic planning", "frequency": 0.18},
          {"topic": "technology trends", "frequency": 0.15}
        ]
      }
    }
  ],
  "generated_at": "2024-01-24T11:00:00Z"
}
```

## Multi-Tenant Endpoints

### Tenant Management (Admin Only)

#### List Tenants

```http
GET /admin/tenants
Authorization: Bearer <admin_token>
```

**Response:**
```json
{
  "tenants": [
    {
      "id": "tenant_uuid",
      "name": "Acme Corporation",
      "subdomain": "acme",
      "custom_domain": "intelligence.acme.com",
      "subscription_tier": "enterprise",
      "user_count": 150,
      "created_at": "2024-01-01T00:00:00Z",
      "status": "active"
    }
  ],
  "total": 25,
  "active": 23,
  "inactive": 2
}
```

#### Create Tenant

```http
POST /admin/tenants
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "name": "New Company Inc",
  "subdomain": "newcompany",
  "custom_domain": "intelligence.newcompany.com",
  "subscription_tier": "compound_intelligence",
  "settings": {
    "branding": {
      "logo_url": "https://newcompany.com/logo.png",
      "primary_color": "#1f2937",
      "accent_color": "#8b5cf6"
    },
    "features": {
      "white_label": true,
      "custom_domain": true,
      "api_access": true
    }
  }
}
```

**Response:**
```json
{
  "id": "tenant_uuid",
  "name": "New Company Inc",
  "subdomain": "newcompany",
  "custom_domain": "intelligence.newcompany.com",
  "subscription_tier": "compound_intelligence",
  "api_key": "objx_api_key_...",
  "created_at": "2024-01-24T11:15:00Z",
  "status": "active"
}
```

### White-Label Configuration

#### Get Tenant Branding

```http
GET /tenant/branding
Authorization: Bearer <token>
```

**Response:**
```json
{
  "branding": {
    "logo_url": "https://client.com/intelligence-logo.png",
    "favicon_url": "https://client.com/favicon.ico",
    "primary_color": "#1a365d",
    "accent_color": "#3182ce",
    "font_family": "Inter, sans-serif",
    "custom_css": "/* Custom styling */\n:root { --primary: #1a365d; }"
  },
  "domain_settings": {
    "custom_domain": "intelligence.client.com",
    "subdomain": "client",
    "ssl_enabled": true
  }
}
```

#### Update Tenant Branding

```http
PUT /tenant/branding
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "branding": {
    "logo_url": "https://client.com/new-logo.png",
    "primary_color": "#2d3748",
    "accent_color": "#4299e1"
  }
}
```

## Webhook Integration

The platform supports webhooks for real-time event notifications.

### Configure Webhooks

```http
POST /webhooks
Authorization: Bearer <token>
Content-Type: application/json

{
  "url": "https://your-app.com/webhooks/objx",
  "events": ["conversation.created", "memory.added", "user.login"],
  "secret": "webhook_secret_key"
}
```

### Webhook Events

#### Conversation Created

```json
{
  "event": "conversation.created",
  "timestamp": "2024-01-24T11:30:00Z",
  "data": {
    "conversation_id": "conversation_uuid",
    "user_id": "user_uuid",
    "tenant_id": "tenant_uuid",
    "first_message": "Analyze market trends"
  }
}
```

#### Memory Added

```json
{
  "event": "memory.added",
  "timestamp": "2024-01-24T11:30:15Z",
  "data": {
    "memory_id": "memory_uuid",
    "content": "Key insight about market trends",
    "user_id": "user_uuid",
    "tenant_id": "tenant_uuid"
  }
}
```

## Rate Limiting

The API implements rate limiting to ensure fair usage and system stability.

### Rate Limits by Tier

| Tier | Requests/Hour | Requests/Day | Burst Limit |
|------|---------------|--------------|-------------|
| Systematic Thinking | 100 | 1,000 | 20/min |
| Compound Intelligence | 500 | 5,000 | 50/min |
| Complete Methodology | 2,000 | 20,000 | 100/min |
| Custom White Label | Unlimited | Unlimited | 500/min |

### Rate Limit Headers

All API responses include rate limit information:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642694400
X-RateLimit-Retry-After: 3600
```

### Rate Limit Exceeded Response

```json
{
  "error": "rate_limit_exceeded",
  "message": "API rate limit exceeded",
  "retry_after": 3600,
  "limit": 100,
  "remaining": 0,
  "reset": 1642694400
}
```

## Error Handling

The API uses standard HTTP status codes and provides detailed error information.

### Error Response Format

```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "details": {
    "field": "specific_error_details"
  },
  "request_id": "req_uuid",
  "timestamp": "2024-01-24T11:45:00Z"
}
```

### Common Error Codes

| Status Code | Error Code | Description |
|-------------|------------|-------------|
| 400 | `bad_request` | Invalid request format or parameters |
| 401 | `unauthorized` | Missing or invalid authentication |
| 403 | `forbidden` | Insufficient permissions |
| 404 | `not_found` | Resource not found |
| 409 | `conflict` | Resource conflict (duplicate, etc.) |
| 422 | `validation_error` | Request validation failed |
| 429 | `rate_limit_exceeded` | API rate limit exceeded |
| 500 | `internal_error` | Internal server error |
| 502 | `bad_gateway` | Upstream service error |
| 503 | `service_unavailable` | Service temporarily unavailable |

### Validation Errors

```json
{
  "error": "validation_error",
  "message": "Request validation failed",
  "details": {
    "email": ["Invalid email format"],
    "password": ["Password must be at least 8 characters"]
  },
  "request_id": "req_uuid",
  "timestamp": "2024-01-24T11:45:00Z"
}
```

## SDK and Libraries

### Python SDK

```python
from objx_intelligence import OBJXClient

# Initialize client
client = OBJXClient(
    api_key="your_api_key",
    base_url="https://api.objx.design/v1"
)

# Send message
response = client.chat.send_message(
    message="Analyze market trends for renewable energy",
    context="quarterly_analysis"
)

print(response.content)
print(response.thinking_process)

# Search memory
memories = client.memory.search(
    query="renewable energy",
    limit=10
)

for memory in memories:
    print(f"{memory.content} (relevance: {memory.relevance_score})")
```

### JavaScript SDK

```javascript
import { OBJXClient } from '@objx/intelligence-sdk';

// Initialize client
const client = new OBJXClient({
  apiKey: 'your_api_key',
  baseURL: 'https://api.objx.design/v1'
});

// Send message
const response = await client.chat.sendMessage({
  message: 'Analyze market trends for renewable energy',
  context: 'quarterly_analysis'
});

console.log(response.content);
console.log(response.thinkingProcess);

// Search memory
const memories = await client.memory.search({
  query: 'renewable energy',
  limit: 10
});

memories.forEach(memory => {
  console.log(`${memory.content} (relevance: ${memory.relevanceScore})`);
});
```

## Testing

### API Testing with cURL

```bash
# Set your API token
export API_TOKEN="your_jwt_token_here"

# Test chat endpoint
curl -X POST https://api.objx.design/v1/chat \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Test message for API validation",
    "context": "api_testing"
  }'

# Test memory search
curl -X POST https://api.objx.design/v1/memory/search \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "test",
    "limit": 5
  }'
```

### Postman Collection

A comprehensive Postman collection is available for API testing:

```json
{
  "info": {
    "name": "OBJX Intelligence Platform API",
    "description": "Complete API collection for testing",
    "version": "1.0.0"
  },
  "auth": {
    "type": "bearer",
    "bearer": [
      {
        "key": "token",
        "value": "{{api_token}}",
        "type": "string"
      }
    ]
  },
  "variable": [
    {
      "key": "base_url",
      "value": "https://api.objx.design/v1"
    },
    {
      "key": "api_token",
      "value": "your_token_here"
    }
  ]
}
```

## Support and Resources

### API Status Page

Monitor API status and uptime at: https://status.objx.design

### Rate Limit Monitoring

Check your current rate limit usage:

```http
GET /account/rate-limits
Authorization: Bearer <token>
```

### API Changelog

Stay updated with API changes at: https://api.objx.design/changelog

### Support Channels

- **Documentation**: https://docs.objx.design/api
- **Community**: https://community.objx.design
- **Support**: api-support@objx.design
- **Status Updates**: https://status.objx.design

This API documentation provides comprehensive coverage of all available endpoints and functionality. For additional examples, advanced use cases, or integration assistance, refer to the platform documentation or contact our support team.

