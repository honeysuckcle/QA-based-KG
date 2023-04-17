import React from "react";
import cover from './pic/cover.jpg';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import { makeStyles } from '@material-ui/core/styles';

let bg_style={
    top: '0',
    left: '0',
    width: document.documentElement.clientWidth,
    height: document.documentElement.clientHeight,
    minWidth: '1000px',
    backgroundRepeat: 'no-repeat',
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    // opacity: 0.9,
}

let button_style={
    color:'#fff',
    margin:'10px',
}

class Home extends React.Component {
    render() {
        const { url } = this.props.match;
        return (
            <div>
                <div style={{zIndex: -10}}>
                    <img src={cover} style={bg_style}/>
                </div>
                <div style={{
                    position:'fixed',
                    top:'38%',
                    left:'50%',
                    transform: 'translate(-50%,-50%)',
                    zIndex:1,
                    color: '#fff',
                    letterSpacing:10,
                    fontSize: '30px',
                    fontFamily:'STKaiti',
                    fontWeight:'lighter',
                    // backgroundColor:'orange',
                }}>
                    <p>基于知识图谱的测试领域的问答系统</p>
                    <div style={{
                        fontSize: '18px',
                        flexGrow: 1,
                        textAlign: 'center',
                        marginTop:'10%',
                    }}>
                        <Grid container spacing={3}>
                            <Grid item xs={6}>
                                <Button size='large' variant="outlined" href={'/user'} style={button_style}>
                                    用户入口
                                </Button>
                            </Grid>
                            <Grid item xs={6}>
                                <Button size='large' variant="outlined" href={'/admin'} style={button_style}>
                                    管理员入口
                                </Button>
                            </Grid>
                        </Grid>

                    </div>
                </div>

            </div>
        );
    }
}

export default Home;
