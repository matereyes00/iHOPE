var wms_layers = [];

var format_rg1baseadminboundsgridcopy_0 = new ol.format.GeoJSON();
var features_rg1baseadminboundsgridcopy_0 = format_rg1baseadminboundsgridcopy_0.readFeatures(json_rg1baseadminboundsgridcopy_0, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_rg1baseadminboundsgridcopy_0 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_rg1baseadminboundsgridcopy_0.addFeatures(features_rg1baseadminboundsgridcopy_0);
var lyr_rg1baseadminboundsgridcopy_0 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_rg1baseadminboundsgridcopy_0, 
                style: style_rg1baseadminboundsgridcopy_0,
                popuplayertitle: "rg1-base-adminbounds-grid copy",
                interactive: true,
                    title: '<img src="styles/legend/rg1baseadminboundsgridcopy_0.png" /> rg1-base-adminbounds-grid copy'
                });
var group_rg1 = new ol.layer.Group({
                                layers: [lyr_rg1baseadminboundsgridcopy_0,],
                                fold: "open",
                                title: "rg1"});

lyr_rg1baseadminboundsgridcopy_0.setVisible(true);
var layersList = [group_rg1];
lyr_rg1baseadminboundsgridcopy_0.set('fieldAliases', {'fid': 'fid', 'bg_name': 'bg_name', 'cm_name': 'cm_name', 'pr_name': 'pr_name', 'Neighbors3': 'Neighbors3', 'Neighbors': 'Neighbors', });
lyr_rg1baseadminboundsgridcopy_0.set('fieldImages', {'fid': 'TextEdit', 'bg_name': 'TextEdit', 'cm_name': 'TextEdit', 'pr_name': 'TextEdit', 'Neighbors3': 'TextEdit', 'Neighbors': 'TextEdit', });
lyr_rg1baseadminboundsgridcopy_0.set('fieldLabels', {'fid': 'no label', 'bg_name': 'no label', 'cm_name': 'no label', 'pr_name': 'no label', 'Neighbors3': 'no label', 'Neighbors': 'no label', });
lyr_rg1baseadminboundsgridcopy_0.on('precompose', function(evt) {
    evt.context.globalCompositeOperation = 'normal';
});