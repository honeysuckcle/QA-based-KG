import './App.css';
import Chat, { Bubble, useMessages } from '@chatui/core';
import '@chatui/core/dist/index.css';
import request from "./helper";

const App = () => {
  const initialMessages = [
    {
      type: 'text',
      content: { text: '请问你有什么问题要问我吗？我一定知无不言~' },
      user: { avatar: 'OIP.jpg' },
    },
  ];

  const { messages, appendMsg, setTyping } = useMessages(initialMessages);

  function handleSend(type, val) {
    if (type === 'text' && val.trim()) {
      appendMsg({
        type: 'text',
        content: { text: val },
        position: 'right',
      });

      setTyping(true);

      request({
        route:'kgbot',
        text: val,
        method:'GET',
        headers:{
          'Content-Type':'text/html; charset=utf-8'
        },
      })
          .then(res => res.text())
          .then(text => {
            console.log(text)
            appendMsg({
              type:'text',
              content:{text:text},
            })
          })

    }
  }

  function renderMessageContent(msg) {
    const { content } = msg;
    return <Bubble content={content.text} />;
  }

  return (
      <Chat
          navbar={{ title: '策问 —— 一个基于知识图谱的测试领域的问答助手' }}
          messages={messages}
          renderMessageContent={renderMessageContent}
          onSend={handleSend}
      />
  );
};

export default App;
