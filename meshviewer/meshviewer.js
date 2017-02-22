/******************** basic viewer for 2D meshes ********************/

function MeshViewer(name)
{
    this._name = name;
    
    this._divElem = 0;
    this._svgElem = 0;
    this._meshElem = 0;
    this._zonesElem = 0;

    this._data = [];

    this._viewBox = [];
    this._viewRes = 0;
    
    this._setupZoom();
    this._setupToolTip();
    
    this._shrink = 0.9;
    this._invShrink = 1 - this._shrink;
    
    // generated from http://tools.medialab.sciences-po.fr/iwanthue/index.php
    this._colors = ["#4a6fb9", "#77b341", "#b05fd3", "#52a976", 
                    "#c84aa9", "#cda549", "#6666d6", "#797832",
                    "#9098df", "#ce423e", "#46b3d1", "#ce417a",
                    "#c9713c", "#8b5494", "#c1656e", "#d989c3"];
}

/******************** public functions ********************/

MeshViewer.prototype.loadData = function(files)
{
    var self = this;  // for anonymous functions
    
    for (var i = 0; i < files.length; ++i) {
        d3.json(files[i], function(error, data) {
            self._data.push(data);
            
            if (self._data.length == files.length) {
                self._setupMesh();
                self._setupZones();
                self._setupViewBox();
            }
        });
    }
}

MeshViewer.prototype.updateViewBox = function()
{
    var vbox = this._viewBox;

    var rect = [parseFloat(this._divElem.style('width')),
                parseFloat(this._divElem.style('height'))];
                
    if (this._viewRes == 0) {
        var rectAR = rect[0] / rect[1];
        var vboxAR = vbox[2] / vbox[3];
        
        if (rectAR < vboxAR) {
            vbox[3] = vbox[2] / rectAR;  // fix width update height
        }
        else if (rectAR > vboxAR) {
            vbox[2] = vbox[3] * rectAR;  // fix height update width
        }
        this._viewRes = vbox[2] / rect[0];
    }
    else {
        vbox[2] = rect[0] * this._viewRes;
        vbox[3] = rect[1] * this._viewRes;
    }
    this._svgElem.attr('viewBox', vbox.join(' '));
}

/******************** protected/private functions ********************/

// linear interpolation between centroid and node
MeshViewer.prototype._shrinkNode = function(mid, node)
{
    return [this._shrink * node[0] + this._invShrink * mid[0],
            this._shrink * node[1] + this._invShrink * mid[1]];
}

// shrink zone geometry towards centroid
MeshViewer.prototype._shrinkZone = function(id)
{
    var mesh = this._data[id[0]];
    var zone = mesh.zones[id[1]];

    // compute centroid of zone
    if (!('mid' in zone)) {
        var val0 = 0, val1 = 0;
        for (var i = 0; i < zone.nids.length; ++i) {
            var pos = mesh.nodes[zone.nids[i]]['pos'];
            val0 += pos[0];
            val1 += pos[1];
        }
        var mid = zone['mid'] = {};
        mid[0] = val0 / zone.nids.length;
        mid[1] = val1 / zone.nids.length;
    }
    var self = this;  // for anonymous functions

    var shrinkFunc = function(mid) {
        return function(id) { return self._shrinkNode(mid, mesh.nodes[id]['pos']); };
    }
    return zone.nids.map(shrinkFunc(zone['mid']));
}

MeshViewer.prototype._createPath = function(id)
{
    // generate closed poly-line path
    var lineFunc = d3.svg.line()
        .x(function(p) { return p[0]; })
        .y(function(p) { return p[1]; })
        .interpolate('linear-closed');
        
    return lineFunc(this._shrinkZone(id));
}

MeshViewer.prototype._updateTransform = function()
{
    var trans = d3.event.translate;
    var transStr = 'translate(' + trans[0] + ',' + trans[1] + ')';

    // flip svg so that y=0 is at bottom: (scale,-scale)
    var scale = d3.event.scale;
    var scaleStr = 'scale(' + scale + ',-' + scale + ')';

    this._meshElem.attr('transform', transStr + scaleStr);
}

MeshViewer.prototype._setupZoom = function()
{
    var self = this;  // for anonymous functions

    // drag + zoom functionality using d3 behavior
    this._zoomListener = d3.behavior.zoom()
        .scaleExtent([0.1, 100])
        .on('zoom', function() { self._updateTransform(); });
}

MeshViewer.prototype._setupToolTip = function()
{
    this._toolTip = d3.select('body').append('div')
        .attr('class', 'tooltip')
        .style('opacity', 0);
}

MeshViewer.prototype._showToolTip = function()
{
    this._toolTip.transition().style('opacity', 100);
}

MeshViewer.prototype._updateToolTip = function(id)
{
    var rect = this._toolTip[0][0].getBoundingClientRect();
    
    this._toolTip//.text('Zone: ' + id[1])
        .html('Rank: ' + this._data[id[0]].rank + '<br/>' + 'Zone: ' + id[1])
        .style('left', (d3.event.pageX - 0.5 * rect.width) + 'px')
        .style('top', (d3.event.pageY - rect.height - 3) + 'px');  // 3px more separation
}

MeshViewer.prototype._hideToolTip = function()
{
    this._toolTip.transition().style('opacity', 0);
}

MeshViewer.prototype._setupMesh = function()
{
    this._divElem = d3.select('#' + this._name);
    
    this._svgElem = this._divElem.append('svg')
        .attr('id', this._name + '_svg')
        .attr('class', 'svgClass')
        .call(this._zoomListener);
    
    this._meshElem = this._svgElem.append('g')
        .attr('id', this._name + '_mesh');
    
    this._zonesElem = this._meshElem.append('g')
        .attr('id', this._name + '_zones')
}

MeshViewer.prototype._getZoneIds = function()
{
    var ids = [];
    for (var n = 0; n < this._data.length; ++n)
        for (var i in this._data[n].zones)
            ids.push([n, i]);
    return ids;
}

MeshViewer.prototype._setupZones = function()
{
    var self = this;  // for anonymous functions

    this._zonesElem.selectAll('.zone')
        .data(this._getZoneIds()).enter()
        .append('path')
        .attr('id', function(id) { return self._name + '_z_' + id[1]; })
        .attr('d', function(id) { return self._createPath(id); })
        .style('fill', function(id) { return self._colors[self._data[id[0]].rank]; })
        .on('mouseover', function() { self._showToolTip(); })
        .on('mousemove', function(id) { self._updateToolTip(id); })
        .on('mouseout', function() { self._hideToolTip(); });
}

MeshViewer.prototype._setupViewBox = function()
{
    var bbox = Object.assign({}, this._data[0].bbox);
    
    for (var i = 1; i < this._data.length; ++i) {
        var b = this._data[i].bbox;
        if (bbox['min0'] > b['min0']) bbox['min0'] = b['min0'];
        if (bbox['max0'] < b['max0']) bbox['max0'] = b['max0'];
        if (bbox['min1'] > b['min1']) bbox['min1'] = b['min1'];
        if (bbox['max1'] < b['max1']) bbox['max1'] = b['max1'];
    }
    this._viewBox = [bbox['min0'],
                    -bbox['max1'],  // flip svg so that y=0 is at bottom
                     bbox['max0'] - bbox['min0'],
                     bbox['max1'] - bbox['min1']];
    
    this.updateViewBox();

    this._meshElem.call(this._zoomListener.event);  // initial updateTransform
}
