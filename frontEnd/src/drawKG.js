import * as d3 from 'd3';
import React, { useEffect } from "react";

export default function Graph(props) {
    const nodes = props.data.nodes;
    const edges = props.data.edges;
    useEffect(() => {

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

        const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(edges).id(d => d.id).distance(150))
            .force('collision', d3.forceCollide(1).strength(0.1))
            .force('charge', d3.forceManyBody().strength(-1000).distanceMax(800))
            .force("center", d3.forceCenter(width / 2, height / 2));

        const svg = d3.select('#graph')
            .style("width", width)
            .style("height", height*0.9);

        const g = svg.append('g'); // 则svg中创建g

        const edgesLine = svg.select('g')
            .selectAll('line')
            .data(edges) // 绑定数据
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
            .data(nodes)
            .enter()
            .append('circle') // 创建圆
            .attr('r', R) // 半径
            .style('fill', '#95A0DA') // 填充颜色
            .style('stroke', '#CABB68') // 边框颜色
            .style('stroke-width', 1) // 边框粗细
            .call(drag);

        const nodesTexts = svg.select('g')
            .selectAll('text')
            .data(nodes)
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
            .data(edges)
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

    });
    return(
        <div className="App">
            <svg id="graph" ></svg>
        </div>
    )
}