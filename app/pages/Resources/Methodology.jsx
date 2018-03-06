import React, {Component} from "react";
import {translate} from "react-i18next";
import {InlineMath, BlockMath} from "react-katex";
import "katex/dist/katex.min.css";

class Methodology extends Component {

  render() {
    const {t} = this.props;
    return (
      <content>
        <h1>{ t("Methodology") }</h1>
        <p>
          In our Economic Complexity measures (RCA, ECI, ECI+, PCI and PCI+ explained below) we considered simultaneously:
        </p>
        <ul>
          <li>Countries with population greater or equal to 1.25 million</li>
          <li>Countries whose traded value is greater or equal than 1 billion</li>
          <li>Products whose traded value is greater or equal than 10 million</li>
        </ul>
        <p>
          The idea here being to avoid distortions.
        </p>

        <h2>{ t("Revealed Compared Advantage (RCA)") }</h2>
        <h4>Which countries make which products?</h4>
        <p>
          When associating countries to products it is important to take into account the size of the export volume of countries and that of the world trade of products. This is because, even for the same product, we expect the volume of exports of a large country like China, to be larger than the volume of exports of a small country like Uruguay. By the same token, we expect the export volume of products that represent a large fraction of world trade, such as cars or footwear, to represent a larger share of a country's exports than products that account for a small fraction of world trade, like cotton seed oil or potato flour.
        </p>
        <p>
          To make countries and products comparable we use Balassa's definition of Revealed Comparative Advantage or RCA. Balassa's definition says that a country has Revealed Comparative Advantage in a product if it exports more than its "fair" share, that is, a share that is equal to the share of total world trade that the product represents. For example, in 2008, with exports of $42 billion, soybeans represented 0.35% of world trade. Of this total, Brazil exported nearly $11 billion, and since Brazil's total exports for that year were $140 billion, soybeans accounted for 7.8% of Brazil's exports. This represents around 22 times Brazil's “fair share” of soybean exports (7.8% divided by 0.35%), so we can say that Brazil has revealed comparative advantage in soybeans.
        </p>

        <h4>How can we express this mathematically?</h4>
        <p>
          Let:
          <ul>
            <li>
              <InlineMath>{String.raw`X_{cp}`}</InlineMath> = the quantity (in USD) of a product <InlineMath>{String.raw`p`}</InlineMath> that a country <InlineMath>{String.raw`c`}</InlineMath> exports
            </li>
            <li><InlineMath>{String.raw`C`}</InlineMath> = number of considered countries</li>
            <li><InlineMath>{String.raw`P`}</InlineMath> = number of considered products</li>
          </ul>
        </p>
        <p>
          Define <InlineMath>{String.raw`RCA_{cp}`}</InlineMath> as:
          <ol>
            <li><InlineMath>{String.raw`RCA_{cp} = \frac{X_{cp}}{\sum _{c} X_{cp}} / \frac{\sum _{p} X_{cp}}{\sum _{c,p} X_{cp}}`}</InlineMath></li>
          </ol>
        </p>
        <p>
          We use this measure to construct a matrix, <InlineMath>{String.raw`M \in \mathbb{R}^{C \times P}`}</InlineMath> that connects each country to the products that it makes.
        </p>
        <p>
          With entries:
          <ol start="2">
            <li><InlineMath>{String.raw`M_{cp} = \begin{cases} 1 &\text{if } RCA_{cp} \geq 1 \\ 0 &\text{otherwise } \end{cases}`}</InlineMath></li>
          </ol>
        </p>
        <p>
          In our research we have played around with cutoff values other than 1 to construct the <InlineMath>{String.raw`M_{cp}`}</InlineMath> matrix and found that our results are robust to these changes.
        </p>

        <h2>{ t("What is Economic Complexity?") }</h2>
        <p>
          We owe to Adam Smith the idea that the division (specialization) of labor is the secret of the wealth of nations. In a modern interpretation, the division of labor into markets and organizations is what allows the knowledge held by few to reach many, making us collectively wiser.
        </p>
        <p>
          The complexity of an economy is related to the multiplicity of useful knowledge embedded in it. Because individuals are limited in what they know, the only way societies can expand their knowledge base is by facilitating the interaction of individuals in increasingly complex networks in order to make products. We can measure economic complexity by the mix of these products that countries are able to make.
        </p>
        <p>
          Some products, like medical imaging devices or jet engines, embed large amounts of knowledge and are the results of very large networks of people and organizations. These products cannot be made in simpler economies that are missing parts of this network’s capability set. Economic complexity, therefore, is expressed in the composition of a country’s productive output and reflects the structures that emerge to hold and combine knowledge.
        </p>

        <h2>{ t("How is Economic Complexity calculated?") }</h2>
        <p>
          We can measure diversity and ubiquity simply by summing over the rows or columns of the matrix <InlineMath>{String.raw`M_{cp}`}</InlineMath>. Formally, we define:
          <ol>
            <li><InlineMath>{String.raw`Diversity = k_{c, o} = \sum_{p}^{ } M_{cp}`}</InlineMath></li>
            <li><InlineMath>{String.raw`Ubiquity = k_{p, o} = \sum_{c}^{ } M_{cp}`}</InlineMath></li>
          </ol>
        </p>
        <p>
          To generate a more accurate measure of the number of capabilities available in a country, or required by a product, we need to correct the information that diversity and ubiquity carry by using each one to correct the other. For countries, this requires us to calculate the average ubiquity of the products that it exports, the average diversity of the countries that make those products and so forth. For products, this requires us to calculate the average diversity of the countries that make them and the average ubiquity of the other products that these countries make. This can be expressed by the recursion:
        </p>
        <ol start="3">
          <li><InlineMath>{String.raw`k_{c, N} = \frac{1}{k_{c, 0}} \sum_{p}^{ } M_{cp} \cdot k_{p, N - 1}`}</InlineMath></li>
          <li><InlineMath>{String.raw`k_{p, N} = \frac{1}{k_{p, 0}} \sum_{c}^{ } M_{cp} \cdot k_{c, N - 1}`}</InlineMath></li>
        </ol>
        <p>
          We then insert (4) into (3) to obtain
        </p>
        <ol start="5">
          <li><InlineMath>{String.raw`k_{c, N} = \frac{1}{k_{c, 0}} \sum_{p}^{ } M_{cp} \frac{1}{k_{c, 0}} \sum_{{c}'}^{ } M_{{c}'p} \cdot k_{{c}', N - 2}`}</InlineMath></li>
          <li><InlineMath>{String.raw`k_{c, N} = \sum_{{c}'}^{ } M_{{c}'p} \cdot k_{{c}', N - 2} \sum \frac{M_{cp}M_{{c}'p}}{k_{c, 0}k_{p, 0}}`}</InlineMath></li>
        </ol>
        <p>and rewrite this as:</p>
        <ol start="7">
          <li><InlineMath>{String.raw`k_{c, N} = \sum_{{c}'}^{ }\tilde{M}_{c{c}'}k_{{c}', N - 2}`}</InlineMath></li>
        </ol>
        <p>where</p>
        <ol start="8">
          <li><InlineMath>{String.raw`\tilde{M}_{c{c}'} = \sum_{p}^{ } \frac{M_{cp}M_{{c}'p}}{k_{c, 0}k_{p, 0}}`}</InlineMath></li>
        </ol>
        <p>
          We note (7) is satisfied when <InlineMath>{String.raw`k_{c, N} = k_{c, N - 2} = 1`}</InlineMath>.This is the eigenvector of <InlineMath>{String.raw`\tilde{M}_{c{c}'}`}</InlineMath> which is associated with the largest eigenvalue. Since this eigenvector is a vector of ones, it is not informative.  We look, instead, for the eigenvector associated with the second largest eigenvalue. This is the eigenvector that captures the largest amount of variance in the system and is our measure of economic complexity.  Hence, we define the Economic Complexity Index (ECI) as:
        </p>
        <ol start="9">
          <li><InlineMath>{String.raw`ECI = \frac{\vec{K} - <\vec{K}> }{stdev\left ( \vec{K} \right )}`}</InlineMath></li>
        </ol>
        <p>
          where &lt; &gt; represents an average, stdev stands for the standard deviation and
        </p>
        <ol start="10">
          <li><InlineMath>{String.raw`\vec{K} = `}</InlineMath>Eigenvector of <InlineMath>{String.raw`\tilde{M}_{c{c}'}`}</InlineMath> associated with the second largest eigenvalue.</li>
        </ol>
        <p>
          Analogously, we define a Product Complexity Index (PCI). Because of the symmetry of the problem, this can be done simply by exchanging the index of countries (c) with that for products (p) in the definitions above. Hence, we define PCI as:
        </p>
        <ol start="11">
          <li><InlineMath>{String.raw`PCI = \frac{\vec{Q} - <\vec{Q}> }{stdev\left ( \vec{Q} \right )}`}</InlineMath></li>
        </ol>
        <ol start="12">
          <li><InlineMath>{String.raw`\vec{Q} = `}</InlineMath>Eigenvector of <InlineMath>{String.raw`\tilde{M}_{p{p}'}`}</InlineMath> associated with the second largest eigenvalue.</li>
        </ol>
      </content>
    );
  }

}

export default translate()(Methodology);
