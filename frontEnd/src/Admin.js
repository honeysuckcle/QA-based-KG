import React, {useEffect} from 'react';
import { fade, makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import ButtonGroup from '@material-ui/core/ButtonGroup';
import TextField from '@material-ui/core/TextField';
import InputBase from '@material-ui/core/InputBase';
import SearchIcon from '@material-ui/icons/Search';
// import Graph from "./drawKG";
import request from "./helper";
import * as d3 from "d3";
// import * as d3 from "d3";

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    paper: {
        padding: theme.spacing(2),
        textAlign: 'center',
        color: theme.palette.text.secondary,
        // height: 480,
    },

    title: {
        flexGrow: 1,
    },
    container:{

    },
    buttonGroup:{
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
        '& > *': {
            margin: theme.spacing(1),
        },
    },
    inputArea:{
        '& .MuiTextField-root': {
            margin: theme.spacing(1),
            width: '50ch',
        },
    },
    left:{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        '& > *': {
            margin: theme.spacing(1),
        },
    },
    right:{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        '& > *': {
            margin: theme.spacing(1),
        },
    },
    input: {
        display: 'none',
    },
    search: {
        position: 'relative',
        borderRadius: theme.shape.borderRadius,
        backgroundColor: fade(theme.palette.common.white, 0.15),
        '&:hover': {
            backgroundColor: fade(theme.palette.common.white, 0.25),
        },
        marginRight: theme.spacing(2),
        marginLeft: 0,
        width: '100%',
        [theme.breakpoints.up('sm')]: {
            marginLeft: theme.spacing(3),
            width: 'auto',
        },
    },
    searchIcon: {
        padding: theme.spacing(0, 2),
        height: '100%',
        position: 'absolute',
        pointerEvents: 'none',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    },
    inputRoot: {
        color: 'inherit',
    },
    inputInput: {
        padding: theme.spacing(1, 1, 1, 0),
        // vertical padding + font size from searchIcon
        paddingLeft: `calc(1em + ${theme.spacing(4)}px)`,
        transition: theme.transitions.create('width'),
        width: '100%',
        [theme.breakpoints.up('md')]: {
            width: '20ch',
        },
    },
    menuButton: {
        marginRight: theme.spacing(2),
    },
}));



export default function Admin() {
    const classes = useStyles();

    //文本框
    const [value, setValue] = React.useState('');
    const handleChange = (event) => {
        setValue(event.target.value);
    };

    const data = {
        nodes : [{id:0, name: "α测试"}, {id :1, name: "评价软件产品的FLURPS"},
            {id:2, name: "发现只有最终用户才能发现的错误"}, {id:3, name: "从用户角度对软件的功能和性能进行测试"},
            {id:4, name: "产品的界面和特色"}, {id:5, name: "软件产品编码结束之时"},
            {id:6, name: "模块(子系统)测试完成之后"}],
        edges : [{source: 0, target: 2, value: '目的', reverse:'的目'},{source: 0, target: 1, value: '目的',reverse:'的目'},
            {source: 0, target: 3, value: '目的',reverse:'的目'}, {source: 0, target: 4, value: '注重点', reverse: '点重注'},
            {source: 0, target: 5, value: '开始于', reverse: '于始开'}, {source: 0, target: 6, value: '开始于',reverse: '于始开'}]
    };
    const [kg, setKG] = React.useState(data);
    const [center, setCenter] = React.useState('α测试');
    const [searchText, setSearchText] = React.useState('');

    //搜索框中的文字实时绑定
    const searchHandleChange = (event) => {
        setSearchText(event.target.value);
    };

    const formatData = (arr) => {
        const data = {
            nodes : [{id:0, name: searchText}],
            edges : [],
        };
        for (let i=0; i<arr.length; i++){
            let node = {id:i+1, name: arr[i][2]};
            data.nodes.push(node)
            let edge = {source: 0, target: i+1, value: arr[i][1]};
            data.edges.push(edge)
        }
        return data;
    }

    //按下enter键
    const onkeydown = (e)=>{
        if (e.keyCode === 13 && searchText != center) {
            console.log(searchText)
            request({
                route:'kg',
                text: searchText,
                method:'GET',
                headers:{
                    'Content-Type':'text/html; charset=utf-8'
                },
            })
                .then(res => res.json())
                .then(dataArr => {
                    console.log(dataArr)
                    const newData = formatData(dataArr)
                    setKG(newData)
                    console.log(newData)
                    draw(newData)
                    setCenter(searchText)
                })

        }
    }

    // useEffect(()=>{
    //     draw()
    // })

    const draw = (data) => {
        function onDragStart(event, d) {
            if (!event.active) {
                simulation.alphaTarget(1) // 设置衰减系数，对节点位置移动过程的模拟，数值越高移动越快，数值范围[0，1]
                    .restart(); // 拖拽节点后，重新启动模拟
            }
            d.fx = d.x;  // d.x是当前位置，d.fx是静止时位置
            d.fy = d.y;
        }

        function dragging(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }

        function onDragEnd(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;    // 解除dragged中固定的坐标
            d.fy = null;
        }

        const drag = d3.drag()
            .on('start', onDragStart)
            .on('drag', dragging) // 拖拽过程
            .on('end', onDragEnd);


        const width = 800;
        const height = 500;

        const simulation = d3.forceSimulation(data.nodes)
            .force("link", d3.forceLink(data.edges).id(d => d.id).distance(150))
            .force('collision', d3.forceCollide(1).strength(0.1))
            .force('charge', d3.forceManyBody().strength(-1000).distanceMax(800))
            .force("center", d3.forceCenter(width / 2, height / 2));

        const svg = d3.select('#graph')
            .style("width", width)
            .style("height", height*0.9);

        const g = svg.append('g'); // 则svg中创建g

        const edgesLine = svg.select('g')
            .selectAll('line')
            .data(data.edges) // 绑定数据
            .enter() // 添加数据到选择集edgepath
            .append('path') // 生成折线
            .attr('d', (d) => { return d && 'M ' + d.source.x + ' ' + d.source.y + ' L ' + d.target.x + ' ' + d.target.y; }) // 遍历所有数据，d表示当前遍历到的数据，返回绘制的贝塞尔曲线
            .attr('id', (d, i) => { return 'edgepath' + i; }) // 设置id，用于连线文字
            .attr('marker-end', 'url(#arrow)') // 根据箭头标记的id号标记箭头
            .style('stroke', '#408CB5') // 颜色
            .style('stroke-width', 1); // 粗细


        const defs = g.append('defs'); // defs定义可重复使用的元素

        const R = 30;

        const arrowheads = defs.append('marker') // 创建箭头
            .attr('id', 'arrow')
            .attr('markerUnits', 'userSpaceOnUse') // 设置为userSpaceOnUse箭头不受连接元素的影响
            .attr('class', 'arrowhead')
            .attr('markerWidth', 20) // viewport
            .attr('markerHeight', 20) // viewport
            .attr('viewBox', '0 0 20 20') // viewBox
            .attr('refX', 9.3 + R) // 偏离圆心距离
            .attr('refY', 5) // 偏离圆心距离
            .attr('orient', 'auto'); // 绘制方向，可设定为：auto（自动确认方向）和 角度值

        arrowheads.append('path')
            .attr('d', 'M0,0 L0,10 L10,5 z') // d: 路径描述，贝塞尔曲线
            .attr('fill', '#6877CA'); // 填充颜色

        const nodesCircle = svg.select('g')
            .selectAll('circle')
            .data(data.nodes)
            .enter()
            .append('circle') // 创建圆
            .attr('r', R) // 半径
            .style('fill', '#95A0DA') // 填充颜色
            .style('stroke', '#CABB68') // 边框颜色
            .style('stroke-width', 1) // 边框粗细
            .call(drag);

        const nodesTexts = svg.select('g')
            .selectAll('text')
            .data(data.nodes)
            .enter()
            .append('text')
            .attr('dy', '.3em') // 偏移量
            .attr('text-anchor', 'middle') // 节点名称放在圆圈中间位置
            .style('fill', 'black') // 颜色
            .style('pointer-events', 'none') // 禁止鼠标事件
            .text((d) => { // 文字内容
                return d && d.name; // 遍历nodes每一项，获取对应的name
            });

        const edgesText = svg.select('g').selectAll('.edgelabel')
            .data(data.edges)
            .enter()
            .append('text') // 为每一条连线创建文字区域
            .attr('class', 'edgelabel')
            .attr('dx', 50)
            .attr('dy', 0);

        edgesText.append('textPath')// 设置文字内容
            .attr('xlink:href', (d, i) => { return '#edgepath' + i; }) // 文字布置在对应id的连线上
            .style('pointer-events', 'none')
            .attr('text-anchor','center')
            .text((d) => d.value);

        simulation.on('tick', () => {
            // 更新节点坐标
            nodesCircle.attr('transform', (d) => {
                return d && 'translate(' + d.x + ',' + d.y + ')';
            });

            // 更新节点文字坐标
            nodesTexts.attr('transform', (d) => {
                return 'translate(' + (d.x) + ',' + d.y + ')';
            });

            // 更新连线位置
            edgesLine.attr('d', (d) => {
                const path = 'M ' + d.source.x + ' ' + d.source.y + ' L ' + d.target.x + ' ' + d.target.y;
                return path;
            });


            // 更新连线文字位置
            // const handleTopologyLinkRotate = (d) => {
            //     return d.source.x < d.target.x ? 0 : 180
            // };
            // edgesText.attr('rotate', handleTopologyLinkRotate);

            edgesText.attr('transform',function(d,i){
                if (d.target.x<d.source.x){
                    let bbox = this.getBBox();
                    let rx = bbox.x+bbox.width/2;
                    let ry = bbox.y+bbox.height/2;
                    return 'rotate(180 '+rx+' '+ry+')';
                }
                else {
                    return 'rotate(0)';
                }
            });
        });

    }

    return (
        <div className={classes.root}>
            <AppBar position="static">
                <Toolbar>
                    <IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="menu">
                        <MenuIcon />
                    </IconButton>
                    <Typography variant="h6" className={classes.title}>
                        管理员主页
                    </Typography>
                    <div className={classes.search}>
                        <div className={classes.searchIcon}>
                            <SearchIcon />
                        </div>
                        <InputBase
                            placeholder="Search…"
                            classes={{
                                root: classes.inputRoot,
                                input: classes.inputInput,
                            }}
                            inputProps={{ 'aria-label': 'search' }}
                            value={searchText}
                            onChange={searchHandleChange}
                            onKeyDown={onkeydown}
                        />
                    </div>
                </Toolbar>
            </AppBar>

            <Grid container spacing={3} className={classes.container}>
                <Grid item xs className={classes.left}>
                    <div className={classes.buttonGroup}>
                        <input
                            accept="text/plain"
                            className={classes.input}
                            id="contained-button-file"
                            multiple
                            type="file"
                        />
                        <label htmlFor="contained-button-file">
                            <Button variant="contained" color="primary" component="span">
                                上传文件
                            </Button>
                        </label>
                        <ButtonGroup color="primary" aria-label="outlined primary button group">
                            <Button>选择分隔符</Button>
                            <Button>添加关系</Button>
                        </ButtonGroup>
                    </div>
                    <form className={classes.inputArea} noValidate autoComplete="off">
                        <div>
                            <TextField
                                id="outlined-multiline-static"
                                label="待添加的三元组"
                                multiline
                                rows={21}
                                variant="outlined"
                                value={value}
                                onChange={handleChange}
                            />
                        </div>
                    </form>

                </Grid>
                <Grid item xs={8} className={classes.right}>
                    <svg id="graph" ></svg>
                </Grid>

            </Grid>
        </div>
    );
}
