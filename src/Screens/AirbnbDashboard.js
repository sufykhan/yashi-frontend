import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Form, Spinner, Alert, Table } from 'react-bootstrap';
import '../myway.css';

const AirbnbDashboard = () => {
    const [loading, setLoading] = useState(false);
    const [insights, setInsights] = useState(null);
    const [error, setError] = useState(null);
    const [location, setLocation] = useState({
        latitude: 40.7128,
        longitude: -74.0060,
        radius_km: 5
    });
    const [propertyConfig, setPropertyConfig] = useState({
        property_type: 'Entire home/apt',
        bedrooms: 2,
        bathrooms: 2,
        accommodates: 4,
        rating: 4.5,
        reviews_count: 50,
        is_superhost: 1,
        instant_bookable: 1
    });

    const analyzeLocation = async () => {
        setLoading(true);
        setError(null);

        try {
            const response = await fetch('http://localhost:5000/api/analyze-location', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    ...location,
                    ...propertyConfig
                }),
            });

            const data = await response.json();

            if (data.success) {
                setInsights(data.insights);
            } else {
                setError('Failed to analyze location');
            }
        } catch (err) {
            setError('Error connecting to API. Make sure the backend server is running.');
        } finally {
            setLoading(false);
        }
    };

    const formatCurrency = (amount) => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(amount);
    };

    return (
        <Container className="mt-5">
            <Row className="mb-4">
                <Col>
                    <h1 className="text-center">Airbnb Price Intelligence Dashboard</h1>
                    <p className="text-center text-muted">
                        Analyze market trends and optimize your pricing strategy
                    </p>
                </Col>
            </Row>

            {error && (
                <Alert variant="danger" onClose={() => setError(null)} dismissible>
                    {error}
                </Alert>
            )}

            {/* Configuration Section */}
            <Row className="mb-4">
                <Col md={6}>
                    <Card>
                        <Card.Header>
                            <h5>Location Settings</h5>
                        </Card.Header>
                        <Card.Body>
                            <Form>
                                <Form.Group className="mb-3">
                                    <Form.Label>Latitude</Form.Label>
                                    <Form.Control
                                        type="number"
                                        step="0.0001"
                                        value={location.latitude}
                                        onChange={(e) => setLocation({...location, latitude: parseFloat(e.target.value)})}
                                    />
                                </Form.Group>
                                <Form.Group className="mb-3">
                                    <Form.Label>Longitude</Form.Label>
                                    <Form.Control
                                        type="number"
                                        step="0.0001"
                                        value={location.longitude}
                                        onChange={(e) => setLocation({...location, longitude: parseFloat(e.target.value)})}
                                    />
                                </Form.Group>
                                <Form.Group className="mb-3">
                                    <Form.Label>Search Radius (km)</Form.Label>
                                    <Form.Control
                                        type="number"
                                        value={location.radius_km}
                                        onChange={(e) => setLocation({...location, radius_km: parseInt(e.target.value)})}
                                    />
                                </Form.Group>
                            </Form>
                        </Card.Body>
                    </Card>
                </Col>

                <Col md={6}>
                    <Card>
                        <Card.Header>
                            <h5>Property Configuration</h5>
                        </Card.Header>
                        <Card.Body>
                            <Form>
                                <Form.Group className="mb-3">
                                    <Form.Label>Property Type</Form.Label>
                                    <Form.Select
                                        value={propertyConfig.property_type}
                                        onChange={(e) => setPropertyConfig({...propertyConfig, property_type: e.target.value})}
                                    >
                                        <option>Entire home/apt</option>
                                        <option>Private room</option>
                                        <option>Shared room</option>
                                        <option>Hotel room</option>
                                    </Form.Select>
                                </Form.Group>
                                <Row>
                                    <Col md={6}>
                                        <Form.Group className="mb-3">
                                            <Form.Label>Bedrooms</Form.Label>
                                            <Form.Control
                                                type="number"
                                                value={propertyConfig.bedrooms}
                                                onChange={(e) => setPropertyConfig({...propertyConfig, bedrooms: parseInt(e.target.value)})}
                                            />
                                        </Form.Group>
                                    </Col>
                                    <Col md={6}>
                                        <Form.Group className="mb-3">
                                            <Form.Label>Bathrooms</Form.Label>
                                            <Form.Control
                                                type="number"
                                                value={propertyConfig.bathrooms}
                                                onChange={(e) => setPropertyConfig({...propertyConfig, bathrooms: parseInt(e.target.value)})}
                                            />
                                        </Form.Group>
                                    </Col>
                                </Row>
                                <Form.Group className="mb-3">
                                    <Form.Check
                                        type="checkbox"
                                        label="Superhost Status"
                                        checked={propertyConfig.is_superhost === 1}
                                        onChange={(e) => setPropertyConfig({...propertyConfig, is_superhost: e.target.checked ? 1 : 0})}
                                    />
                                </Form.Group>
                            </Form>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>

            <Row className="mb-4">
                <Col className="text-center">
                    <Button
                        variant="primary"
                        size="lg"
                        onClick={analyzeLocation}
                        disabled={loading}
                    >
                        {loading ? (
                            <>
                                <Spinner animation="border" size="sm" className="me-2" />
                                Analyzing...
                            </>
                        ) : (
                            'Analyze Market & Get Insights'
                        )}
                    </Button>
                </Col>
            </Row>

            {/* Results Section */}
            {insights && (
                <>
                    {/* Revenue Projection */}
                    <Row className="mb-4">
                        <Col>
                            <Card className="shadow">
                                <Card.Header className="bg-success text-white">
                                    <h4>Annual Revenue Projection</h4>
                                </Card.Header>
                                <Card.Body>
                                    <Row className="text-center">
                                        <Col md={3}>
                                            <h2 className="text-success">{formatCurrency(insights.revenue_projection.annual_gross_revenue)}</h2>
                                            <p className="text-muted">Gross Revenue</p>
                                        </Col>
                                        <Col md={3}>
                                            <h2 className="text-danger">-{formatCurrency(insights.revenue_projection.estimated_expenses)}</h2>
                                            <p className="text-muted">Est. Expenses</p>
                                        </Col>
                                        <Col md={3}>
                                            <h2 className="text-primary">{formatCurrency(insights.revenue_projection.estimated_net_revenue)}</h2>
                                            <p className="text-muted">Net Revenue</p>
                                        </Col>
                                        <Col md={3}>
                                            <h2>{formatCurrency(insights.revenue_projection.average_monthly_revenue)}</h2>
                                            <p className="text-muted">Avg Monthly</p>
                                        </Col>
                                    </Row>
                                </Card.Body>
                            </Card>
                        </Col>
                    </Row>

                    {/* Pricing Strategy */}
                    <Row className="mb-4">
                        <Col>
                            <Card>
                                <Card.Header>
                                    <h4>Monthly Pricing Strategy</h4>
                                </Card.Header>
                                <Card.Body>
                                    <Table striped bordered hover responsive>
                                        <thead>
                                            <tr>
                                                <th>Month</th>
                                                <th>Recommended Price</th>
                                                <th>Market Average</th>
                                                <th>Position</th>
                                                <th>Demand</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {insights.pricing_strategy.monthly_prices.map((month) => (
                                                <tr key={month.month}>
                                                    <td><strong>{month.month_name}</strong></td>
                                                    <td className="text-success">
                                                        <strong>{formatCurrency(month.recommended_price)}</strong>
                                                    </td>
                                                    <td>{formatCurrency(month.market_average)}</td>
                                                    <td>
                                                        <span className={month.competitive_position === 'above' ? 'text-success' : 'text-warning'}>
                                                            {month.competitive_position === 'above' ? '↑ Above' : '↓ Below'}
                                                        </span>
                                                    </td>
                                                    <td>
                                                        <span className={`badge bg-${
                                                            month.demand_level === 'High' ? 'danger' :
                                                            month.demand_level === 'Medium' ? 'warning' : 'secondary'
                                                        }`}>
                                                            {month.demand_level}
                                                        </span>
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </Table>

                                    <Row className="mt-3">
                                        <Col md={6}>
                                            <Alert variant="success">
                                                <strong>Best Month:</strong> {insights.pricing_strategy.best_month.month_name}
                                                ({formatCurrency(insights.pricing_strategy.best_month.recommended_price)}/night)
                                            </Alert>
                                        </Col>
                                        <Col md={6}>
                                            <Alert variant="info">
                                                <strong>Slowest Month:</strong> {insights.pricing_strategy.worst_month.month_name}
                                                ({formatCurrency(insights.pricing_strategy.worst_month.recommended_price)}/night)
                                            </Alert>
                                        </Col>
                                    </Row>
                                </Card.Body>
                            </Card>
                        </Col>
                    </Row>

                    {/* Market Comparison */}
                    <Row className="mb-4">
                        <Col md={6}>
                            <Card>
                                <Card.Header>
                                    <h5>Market Comparison</h5>
                                </Card.Header>
                                <Card.Body>
                                    <p><strong>Similar Properties:</strong> {insights.market_comparison.similar_properties_count}</p>
                                    <Table bordered size="sm">
                                        <tbody>
                                            <tr>
                                                <td>Average Price</td>
                                                <td><strong>{formatCurrency(insights.market_comparison.market_stats.average_price)}</strong></td>
                                            </tr>
                                            <tr>
                                                <td>Median Price</td>
                                                <td><strong>{formatCurrency(insights.market_comparison.market_stats.median_price)}</strong></td>
                                            </tr>
                                            <tr>
                                                <td>Price Range</td>
                                                <td>
                                                    {formatCurrency(insights.market_comparison.market_stats.min_price)} -
                                                    {formatCurrency(insights.market_comparison.market_stats.max_price)}
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>Avg Rating</td>
                                                <td>{insights.market_comparison.average_rating.toFixed(2)} ⭐</td>
                                            </tr>
                                            <tr>
                                                <td>Avg Occupancy</td>
                                                <td>{insights.market_comparison.average_occupancy.toFixed(1)}%</td>
                                            </tr>
                                        </tbody>
                                    </Table>
                                </Card.Body>
                            </Card>
                        </Col>

                        <Col md={6}>
                            <Card>
                                <Card.Header>
                                    <h5>Optimal Features</h5>
                                </Card.Header>
                                <Card.Body>
                                    <h6>Top Property Types:</h6>
                                    <ul>
                                        {insights.optimal_features.property_types.slice(0, 3).map((type, index) => (
                                            <li key={index}>
                                                <strong>{type.type}</strong>: {formatCurrency(type.average_price)}/night
                                            </li>
                                        ))}
                                    </ul>

                                    <h6 className="mt-3">Price Premiums:</h6>
                                    <Alert variant="success">
                                        <strong>Superhost Premium:</strong> +{formatCurrency(insights.optimal_features.superhost_premium)}/night
                                    </Alert>
                                    <Alert variant="info">
                                        <strong>High Rating Premium:</strong> +{formatCurrency(insights.optimal_features.rating_premium)}/night
                                    </Alert>
                                </Card.Body>
                            </Card>
                        </Col>
                    </Row>

                    {/* Recommendations */}
                    <Row className="mb-4">
                        <Col>
                            <Card>
                                <Card.Header className="bg-primary text-white">
                                    <h4>Actionable Recommendations</h4>
                                </Card.Header>
                                <Card.Body>
                                    {insights.recommendations.map((rec, index) => (
                                        <Card key={index} className="mb-3 border-start border-5"
                                            style={{borderColor: rec.priority === 'High' ? '#dc3545' : '#ffc107'}}>
                                            <Card.Body>
                                                <Row>
                                                    <Col md={8}>
                                                        <h5>
                                                            {rec.title}
                                                            <span className={`badge bg-${rec.priority === 'High' ? 'danger' : 'warning'} ms-2`}>
                                                                {rec.priority}
                                                            </span>
                                                        </h5>
                                                        <p className="text-muted mb-2"><strong>Category:</strong> {rec.category}</p>
                                                        <p>{rec.description}</p>
                                                    </Col>
                                                    <Col md={4}>
                                                        <div className="bg-light p-3 rounded">
                                                            <strong>Action:</strong>
                                                            <p className="mt-2 mb-0">{rec.action}</p>
                                                        </div>
                                                    </Col>
                                                </Row>
                                            </Card.Body>
                                        </Card>
                                    ))}
                                </Card.Body>
                            </Card>
                        </Col>
                    </Row>
                </>
            )}
        </Container>
    );
};

export default AirbnbDashboard;
