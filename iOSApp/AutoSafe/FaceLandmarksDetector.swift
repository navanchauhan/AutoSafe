//
//  FaceLandmarksDetector.swift
//  AutoSafe
//
//  Created by Navan Chauhan on 26/05/19.
//  Copyright © 2019 Navan Chauhan. All rights reserved.
//

import AVFoundation
import UIKit
import Vision

class FaceLandmarksDetector {
    var counter = 0
    open func highlightFaces(for source: UIImage, complete: @escaping (UIImage) -> Void) {
        var resultImage = source
        let detectFaceRequest = VNDetectFaceLandmarksRequest { (request, error) in
            if error == nil {
                if let results = request.results as? [VNFaceObservation] {
                    for faceObservation in results {
                        guard let landmarks = faceObservation.landmarks else {
                            continue
                        }
                        let boundingRect = faceObservation.boundingBox
                        
                        resultImage = self.drawOnImage(source: resultImage, boundingRect: boundingRect, faceLandmarks: landmarks)
                    }
                }
            } else {
                print(error!.localizedDescription)
            }
            complete(resultImage)
        }
        
        let vnImage = VNImageRequestHandler(cgImage: source.cgImage!, options: [:])
        try? vnImage.perform([detectFaceRequest])
    }
    
    private func drawOnImage(source: UIImage, boundingRect: CGRect, faceLandmarks: VNFaceLandmarks2D) -> UIImage {
        UIGraphicsBeginImageContextWithOptions(source.size, false, 1)
        let context = UIGraphicsGetCurrentContext()!
        context.translateBy(x: 0.0, y: source.size.height)
        context.scaleBy(x: 1.0, y: -1.0)
        //context.setBlendMode(CGBlendMode.colorBurn)
        context.setLineJoin(.round)
        context.setLineCap(.round)
        context.setShouldAntialias(true)
        context.setAllowsAntialiasing(true)
        
        let rectWidth = source.size.width * boundingRect.size.width
        let rectHeight = source.size.height * boundingRect.size.height
        
        //draw image
        let rect = CGRect(x: 0, y:0, width: source.size.width, height: source.size.height)
        context.draw(source.cgImage!, in: rect)
        
        
        //draw bound rect
        context.setStrokeColor(UIColor.green.cgColor)
        context.addRect(CGRect(x: boundingRect.origin.x * source.size.width, y:boundingRect.origin.y * source.size.height, width: rectWidth, height: rectHeight))
        context.drawPath(using: CGPathDrawingMode.stroke)
        
        //draw overlay
        context.setLineWidth(1.0)
        
        func drawFeature(_ feature: VNFaceLandmarkRegion2D, color: CGColor, close: Bool = false) {
            context.setStrokeColor(color)
            context.setFillColor(color)
            for point in feature.normalizedPoints {
                // Draw DEBUG numbers
                let textFontAttributes = [
                    NSAttributedString.Key.font: UIFont.systemFont(ofSize: 16),
                    NSAttributedString.Key.foregroundColor: UIColor.white
                ]
                context.saveGState()
                // rotate to draw numbers
                context.translateBy(x: 0.0, y: source.size.height)
                context.scaleBy(x: 1.0, y: -1.0)
                let mp = CGPoint(x: boundingRect.origin.x * source.size.width + point.x * rectWidth, y: source.size.height - (boundingRect.origin.y * source.size.height + point.y * rectHeight))
                context.fillEllipse(in: CGRect(origin: CGPoint(x: mp.x-2.0, y: mp.y-2), size: CGSize(width: 4.0, height: 4.0)))
                if let index = feature.normalizedPoints.firstIndex(of: point) {
                    NSString(format: "%d", index).draw(at: mp, withAttributes: textFontAttributes);
                    //print(mp, index);
                }
                context.restoreGState()
            }
            let mappedPoints = feature.normalizedPoints.map { CGPoint(x: boundingRect.origin.x * source.size.width + $0.x * rectWidth, y: boundingRect.origin.y * source.size.height + $0.y * rectHeight) }
            context.addLines(between: mappedPoints)
            if close, let first = mappedPoints.first, let lats = mappedPoints.last {
                context.addLines(between: [lats, first])
            }
            context.strokePath()
        }
        
        
        if let leftEye = faceLandmarks.leftEye {
            drawFeature(leftEye, color: UIColor.cyan.cgColor, close: true)
            /*
             for point in leftEye.normalizedPoints {
             let mp = CGPoint(x: boundingRect.origin.x * source.size.width + point.x * rectWidth, y: source.size.height - (boundingRect.origin.y * source.size.height + point.y * rectHeight))
             /*
             if let index = leftEye.normalizedPoints.index(of: point) {
             print(mp, index);
             if(index==4){
             print("fuck me, this works!!!")
             point4.append(mp[0])
             } */
             
             }
             
             //for i in leftEye.normalizedPoints{
             //    print("HEHE:")
             //    print(i)
             //}
             */
            //let p1.x = leftEye.normalizedPoints[0].x;
            
            
        }
        if let rightEye = faceLandmarks.rightEye {
            drawFeature(rightEye, color: UIColor.cyan.cgColor, close: true)
            
        }
        if let leftPupil = faceLandmarks.leftPupil {
            drawFeature(leftPupil, color: UIColor.cyan.cgColor, close: true)
        }
        if let rightPupil = faceLandmarks.rightPupil {
            drawFeature(rightPupil, color: UIColor.cyan.cgColor, close: true)
        }
        
        
        
        if let leftEye = faceLandmarks.leftEye, let rightEye = faceLandmarks.rightEye {
            print("WORKS?")
            
            let p1l = leftEye.normalizedPoints[1]
            let p2l = leftEye.normalizedPoints[7]
            
            let p3l = leftEye.normalizedPoints[3]
            let p4l = leftEye.normalizedPoints[5]
            
            let p5l = leftEye.normalizedPoints[0]
            let p6l = leftEye.normalizedPoints[4]
            
            let Al = hypotf(Float(p1l.x - p2l.x), Float(p1l.y - p2l.y));
            let Bl = hypotf(Float(p3l.x - p4l.x), Float(p3l.y - p4l.y));
            let Cl = hypotf(Float(p5l.x - p6l.x), Float(p5l.y - p6l.y));
            
            let leftEAR = (Al + Bl) / (2.0 * Cl)
            
            print("Left EAR", leftEAR);
            
            let p1r = rightEye.normalizedPoints[1]
            let p2r = rightEye.normalizedPoints[7]
            
            let p3r = rightEye.normalizedPoints[3]
            let p4r = rightEye.normalizedPoints[5]
            
            let p5r = rightEye.normalizedPoints[0]
            let p6r = rightEye.normalizedPoints[4]
            
            let Ar = hypotf(Float(p1r.x - p2r.x), Float(p1r.y - p2r.y));
            let Br = hypotf(Float(p3r.x - p4r.x), Float(p3r.y - p4r.y));
            let Cr = hypotf(Float(p5r.x - p6r.x), Float(p5r.y - p6r.y));
            
            let rightEAR = (Ar + Br) / (2.0 * Cr)
            
            print("Right EAR", rightEAR);
            
            let EAR = (Float(leftEAR) + Float(rightEAR)) / 2.0
            print("EAR:", EAR)
            
            let threshold = Float(0.25)
            let noOfFrames = 2
            
            if EAR < threshold {
                counter += 1;
            }
            if EAR > threshold {
                counter -= 1;
            }
            if counter > noOfFrames {
                print("Wake up Sid!")
                AudioServicesPlayAlertSound(SystemSoundID(1005))
                counter = 0
                
            }
        }
        let coloredImg : UIImage = UIGraphicsGetImageFromCurrentImageContext()!
        UIGraphicsEndImageContext()
        return coloredImg
    }
}



