

package main


import "time"

type Stats struct {
	min float64
	max float64
	mean float64
	lower_quartile float64
	upper_quartile float64
	sum float64
}

type AggregationField struct {
	name string
	statistics []Stats
	interval int // In miliseconds
	last_update time.Time
	max_aggregated_samples int
}

type AggregationTempField struct {
	vals []float64
	started_at time.Time
	ended_at time.Time
}

func replaceAggregation(field *AggregationField, temp *AggregationTempField) *AggregationTempField {
	// Construct a stats
	// Put stats on the field
	// Make new temp
	stats := Stats{}
	// Make the sum
	for _, x := range temp.vals {
		stats.sum += x
		// TODO: More stats!
	}
	// Add the stats
	field.statistics = append(field.statistics,stats)
	// if stats is longer than recommended, then prune the earliest. 
	if len(field.statistics) > field.max_aggregated_samples {
		field.statistics = field.statistics[1:]
	}
	// Update the field's last updated time
	field.last_update = time.Now()
	next_agg := AggregationTempField{}
	next_agg.started_at = time.Now()
	next_agg.ended_at = time.Now().Add(time.Second * time.Duration(field.interval))
	return &next_agg
}
func aggregateData(field *AggregationField, temp *AggregationTempField, data float64) {
	if time.Now().After(temp.ended_at) {
		temp = replaceAggregation(field,temp)
		// We better hope that this is not called indefinitely.
		aggregateData(field, temp, data)
		return
	}
	// Otherwise, we should add the data to the current field.
	temp.vals = append(temp.vals, data)
}
