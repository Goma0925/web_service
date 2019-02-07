/*!
 * jquery.ymdpulldown.js v0.1.0
 * Auto to enter the specified numerical value
 * License : MIT
 * Author : Tadashi Suyama<info@its-office.jp> (http://its-office.jp/)
 */

;(function (factory) {
  'use strict';
  if (typeof define === 'function' && define.amd) {
    define(['jquery'], factory);
  } else if (typeof exports === 'object') {
    module.exports = factory(require('jquery'));
  } else {
    factory(jQuery);
  }
}(function($) {
	'use strict';
	var optionLoop, this_day, this_month, this_year, today;

	// 本日の日付け年月日で取得
	today = new Date();
	this_year = today.getFullYear();
	this_month = today.getMonth() + 1;
	this_day = today.getDate();
	/*
	ループ処理（スタート数字、終了数字、デフォルト数字）
	 */
	optionLoop = function(start, end, defaults) {
		var i, opt;
		opt = null;
		for (i = start; i <= end ; i++) {
			if (i === defaults) {
				opt += "<option value='" + i + "' selected>" + i + "</option>";
			} else {
				opt += "<option value='" + i + "'>" + i + "</option>";
			}
		}
		return opt;
	};

	$.fn.ymdpulldown = function(options){

		var elements = this;
		var defaults = {
			year  : this_year,
			month : this_month,
			day   : this_day,
			startyear : 1950,
			start  : 100,
			end    : 200,
			select : null,
			choice : null // year,month,day,other
		};

		elements.each(function() {
			var opts = $.extend({}, defaults, options, $(this).data());
			var loop;
			if (opts.choice === 'year') {
				loop = optionLoop(opts.startyear, opts.year, opts.select);
			} else if(opts.choice === 'month'){
				loop = optionLoop(1, 12, opts.select);
			} else if(opts.choice === 'day'){
				loop = optionLoop(1, 31, opts.select);
			} else {
				loop = optionLoop(opts.start, opts.end, opts.select);
			}
			$(this).append(loop);
		});
	};
}));

