/**
 * Feishu Calendar Add Event Tool
 * 飞书日历添加日程工具
 */

const { getAccessToken, getCalendars } = require('./calendar-client');

async function addEvent(summary, startTimeStr, endTimeStr, description = '') {
  try {
    const token = await getAccessToken();
    const calendars = await getCalendars(token);
    const primaryCalendar = calendars.find(c => c.is_primary) || calendars[0];
    
    // 解析时间 (格式: YYYY-MM-DD HH:MM)
    const start = new Date(startTimeStr);
    const end = new Date(endTimeStr);
    
    const event = {
      summary: summary,
      description: description,
      start_time: { 
        timestamp: String(Math.floor(start.getTime() / 1000)), 
        timezone: 'Asia/Shanghai' 
      },
      end_time: { 
        timestamp: String(Math.floor(end.getTime() / 1000)), 
        timezone: 'Asia/Shanghai' 
      },
      reminders: [
        { minutes: 10 } // 默认提前10分钟提醒
      ]
    };

    const response = await fetch(`https://open.feishu.cn/open-apis/calendar/v4/calendars/${primaryCalendar.calendar_id}/events`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(event)
    });

    const data = await response.json();
    if (data.code !== 0) {
      throw new Error(`创建日程失败: ${data.msg}`);
    }

    return data.data.event;
  } catch (error) {
    console.error('❌ 错误:', error.message);
    throw error;
  }
}

// 命令行参数处理
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length < 3) {
    console.log('用法: node add-event.js <标题> <开始时间> <结束时间> [描述]');
    console.log('示例: node add-event.js "录制视频" "2026-03-08 15:00" "2026-03-08 16:00"');
    process.exit(1);
  }

  const [summary, start, end, desc] = args;
  addEvent(summary, start, end, desc).then(event => {
    console.log(`✅ 日程创建成功: ${event.summary}`);
    console.log(`🆔 ID: ${event.event_id}`);
  }).catch(err => {
    console.error(err);
    process.exit(1);
  });
}
