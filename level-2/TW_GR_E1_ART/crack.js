ans = Array.from(new Array(83), (_, idx) => {
					if (idx >= 2) {
						idx++
					}

					if (idx >= 77) {
						idx++;
					}

					var r = Math.floor(idx / 5) + 1;
					var c = (idx % 5) + 1;

					return createFlag(idx, { r: r, c: c });
				})
ans.forEach(function(element) {
    if (element.effects[0].check == 64){
       window.alert(element.location.c+" , "+element.location.r);
    }
});
